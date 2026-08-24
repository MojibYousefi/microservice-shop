import os
import sys
import json
from contextlib import asynccontextmanager
from typing import List, Optional
import redis.asyncio as aioredis
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.shared.config import settings
from backend.shared.database import init_db, get_async_session
from backend.shared.redis import get_redis, close_redis
from backend.shared.models import (
    Order, OrderItem, OrderRead, OrderItemRead,
    Product, CartItem, CartRead, CartItemAdd, OrderCreate
)
from backend.shared.security import get_current_user_payload


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_redis()


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Order & Cart Service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "order_service", "debug": settings.DEBUG}


# Helper for Redis cart key
def get_cart_key(user_id: int) -> str:
    return f"cart:user:{user_id}"


# ==========================================
# Async Redis Cart Endpoints
# ==========================================

@app.get("/api/v1/cart/{user_id}", response_model=CartRead)
async def get_cart(
    user_id: int,
    redis: aioredis.Redis = Depends(get_redis)
):
    key = get_cart_key(user_id)
    try:
        raw_items = await redis.hgetall(key)
    except Exception:
        # Graceful fallback if Redis is unavailable in local sandbox testing
        raw_items = {}

    items: List[CartItem] = []
    total_price = 0.0

    for product_id_str, item_json in raw_items.items():
        data = json.loads(item_json)
        item = CartItem(**data)
        items.append(item)
        total_price += item.price * item.quantity

    return CartRead(user_id=user_id, items=items, total_price=round(total_price, 2))


@app.post("/api/v1/cart/{user_id}", response_model=CartRead)
async def add_to_cart(
    user_id: int,
    item_add: CartItemAdd,
    db: AsyncSession = Depends(get_async_session),
    redis: aioredis.Redis = Depends(get_redis)
):
    # Fetch product details from DB
    stmt = select(Product).where(Product.id == item_add.product_id)
    res = await db.exec(stmt)
    product = res.first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    if product.stock < item_add.quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock. Only {product.stock} available.")

    key = get_cart_key(user_id)
    existing_raw = await redis.hget(key, str(product.id))

    current_qty = 0
    if existing_raw:
        existing_data = json.loads(existing_raw)
        current_qty = existing_data.get("quantity", 0)

    new_qty = current_qty + item_add.quantity

    cart_item = CartItem(
        product_id=product.id,
        title=product.title,
        price=product.price,
        quantity=new_qty,
        image_url=product.image_url
    )

    try:
        await redis.hset(key, str(product.id), json.dumps(cart_item.model_dump()))
    except Exception as e:
        if not settings.DEBUG:
            raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

    return await get_cart(user_id, redis)


@app.delete("/api/v1/cart/{user_id}/items/{product_id}", response_model=CartRead)
async def remove_from_cart(
    user_id: int,
    product_id: int,
    redis: aioredis.Redis = Depends(get_redis)
):
    key = get_cart_key(user_id)
    try:
        await redis.hdel(key, str(product_id))
    except Exception:
        pass
    return await get_cart(user_id, redis)


@app.delete("/api/v1/cart/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    user_id: int,
    redis: aioredis.Redis = Depends(get_redis)
):
    key = get_cart_key(user_id)
    try:
        await redis.delete(key)
    except Exception:
        pass
    return None


# ==========================================
# Async Order Endpoints
# ==========================================

@app.post("/api/v1/orders", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: Optional[OrderCreate] = None,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_async_session),
    redis: aioredis.Redis = Depends(get_redis)
):
    user_id = payload.get("user_id", 1)

    items_to_order = []

    # If items passed in payload, use them. Otherwise load from Redis cart.
    if order_in and order_in.items:
        for item_req in order_in.items:
            stmt = select(Product).where(Product.id == item_req.product_id)
            res = await db.exec(stmt)
            prod = res.first()
            if not prod:
                raise HTTPException(status_code=404, detail=f"Product {item_req.product_id} not found.")
            if prod.stock < item_req.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {prod.title}.")
            items_to_order.append({
                "product": prod,
                "quantity": item_req.quantity
            })
    else:
        # Fetch cart from Redis
        key = get_cart_key(user_id)
        try:
            raw_items = await redis.hgetall(key)
        except Exception:
            raw_items = {}

        if not raw_items:
            raise HTTPException(status_code=400, detail="Cart is empty.")

        for prod_id_str, raw_json in raw_items.items():
            cart_item_data = json.loads(raw_json)
            prod_id = cart_item_data["product_id"]
            qty = cart_item_data["quantity"]

            stmt = select(Product).where(Product.id == prod_id)
            res = await db.exec(stmt)
            prod = res.first()

            if not prod or prod.stock < qty:
                raise HTTPException(status_code=400, detail=f"Product unavailable or out of stock.")
            items_to_order.append({
                "product": prod,
                "quantity": qty
            })

    # Calculate total price & decrement stock
    total_price = 0.0
    order_items_objs = []

    for item_data in items_to_order:
        prod: Product = item_data["product"]
        qty: int = item_data["quantity"]

        item_price = prod.price * qty
        total_price += item_price

        # Update product stock
        prod.stock -= qty
        db.add(prod)

        order_items_objs.append({
            "product_id": prod.id,
            "product_title": prod.title,
            "price": prod.price,
            "quantity": qty
        })

    # Create Order
    db_order = Order(
        user_id=user_id,
        total_price=round(total_price, 2),
        status="paid"
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Create Order Items
    item_reads = []
    for item_dict in order_items_objs:
        db_item = OrderItem(
            order_id=db_order.id,
            **item_dict
        )
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        item_reads.append(OrderItemRead(
            id=db_item.id,
            product_id=db_item.product_id,
            product_title=db_item.product_title,
            price=db_item.price,
            quantity=db_item.quantity
        ))

    # Clear Redis cart
    key = get_cart_key(user_id)
    try:
        await redis.delete(key)
    except Exception:
        pass

    return OrderRead(
        id=db_order.id,
        user_id=db_order.user_id,
        total_price=db_order.total_price,
        status=db_order.status,
        created_at=db_order.created_at,
        items=item_reads
    )


@app.get("/api/v1/orders", response_model=List[OrderRead])
async def list_orders(
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    user_id = payload.get("user_id", 1)
    stmt = select(Order).where(Order.user_id == user_id).order_by(Order.id.desc())
    res = await db.exec(stmt)
    orders = res.all()

    result = []
    for ord_obj in orders:
        stmt_items = select(OrderItem).where(OrderItem.order_id == ord_obj.id)
        res_items = await db.exec(stmt_items)
        items = res_items.all()

        item_reads = [
            OrderItemRead(
                id=item.id,
                product_id=item.product_id,
                product_title=item.product_title,
                price=item.price,
                quantity=item.quantity
            ) for item in items
        ]

        result.append(OrderRead(
            id=ord_obj.id,
            user_id=ord_obj.user_id,
            total_price=ord_obj.total_price,
            status=ord_obj.status,
            created_at=ord_obj.created_at,
            items=item_reads
        ))

    return result


@app.get("/api/v1/orders/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    payload: dict = Depends(get_current_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    user_id = payload.get("user_id", 1)
    stmt = select(Order).where(Order.id == order_id, Order.user_id == user_id)
    res = await db.exec(stmt)
    ord_obj = res.first()
    if not ord_obj:
        raise HTTPException(status_code=404, detail="Order not found.")

    stmt_items = select(OrderItem).where(OrderItem.order_id == ord_obj.id)
    res_items = await db.exec(stmt_items)
    items = res_items.all()

    item_reads = [
        OrderItemRead(
            id=item.id,
            product_id=item.product_id,
            product_title=item.product_title,
            price=item.price,
            quantity=item.quantity
        ) for item in items
    ]

    return OrderRead(
        id=ord_obj.id,
        user_id=ord_obj.user_id,
        total_price=ord_obj.total_price,
        status=ord_obj.status,
        created_at=ord_obj.created_at,
        items=item_reads
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.ORDER_SERVICE_PORT)
