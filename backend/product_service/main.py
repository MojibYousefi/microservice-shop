import os
import sys
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.shared.config import settings
from backend.shared.database import init_db, get_async_session, async_session_maker
from backend.shared.models import (
    Category, CategoryCreate, CategoryRead,
    Product, ProductCreate, ProductUpdate, ProductRead
)
from backend.shared.security import get_current_admin_user_payload


async def seed_initial_data():
    """
    Seeds initial e-commerce categories and products asynchronously if database is empty.
    """
    async with async_session_maker() as session:
        stmt = select(Category)
        res = await session.exec(stmt)
        if res.first() is not None:
            return  # Already seeded

        # Create initial categories
        electronics = Category(name="Electronics", slug="electronics", description="Gadgets, computers and tech gear")
        fashion = Category(name="Fashion & Apparel", slug="fashion", description="Clothing, shoes and luxury wear")
        home = Category(name="Home & Living", slug="home-living", description="Furniture, decor and kitchen essentials")

        session.add_all([electronics, fashion, home])
        await session.commit()
        await session.refresh(electronics)
        await session.refresh(fashion)
        await session.refresh(home)

        # Create initial products with high-quality visual images
        products = [
            Product(
                title="Aura Pro Wireless Headphones",
                description="Active noise canceling studio headphones with spatial audio and 40-hour battery life.",
                price=249.99,
                stock=50,
                image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80",
                category_id=electronics.id
            ),
            Product(
                title="Vanguard Mechanical Keyboard",
                description="Ultra-responsive RGB mechanical gaming keyboard with hot-swappable tactile switches.",
                price=129.50,
                stock=30,
                image_url="https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80",
                category_id=electronics.id
            ),
            Product(
                title="Minimalist Urban Watch",
                description="Sleek stainless steel quartz watch with sapphire glass and genuine leather strap.",
                price=189.00,
                stock=25,
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
                category_id=fashion.id
            ),
            Product(
                title="Ergonomic Executive Chair",
                description="Breathable mesh ergonomic desk chair with lumbar support and customizable armrests.",
                price=349.00,
                stock=15,
                image_url="https://images.unsplash.com/photo-1580481072645-022f9a6d8310?auto=format&fit=crop&w=800&q=80",
                category_id=home.id
            ),
            Product(
                title="Smart OLED Ambient Lamp",
                description="App-controlled RGB ambient light bar with dynamic music synchronization.",
                price=79.99,
                stock=40,
                image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80",
                category_id=home.id
            ),
        ]
        session.add_all(products)
        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_initial_data()
    yield


app = FastAPI(
    title=f"{settings.PROJECT_NAME} - Product Service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "product_service", "debug": settings.DEBUG}


# ==========================================
# Category Endpoints
# ==========================================

@app.get("/api/v1/categories", response_model=List[CategoryRead])
async def list_categories(
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(Category)
    res = await db.exec(stmt)
    return res.all()


@app.post("/api/v1/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    cat_in: CategoryCreate,
    admin_payload: dict = Depends(get_current_admin_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    category = Category(
        name=cat_in.name,
        slug=cat_in.slug,
        description=cat_in.description
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


# ==========================================
# Product Endpoints
# ==========================================

@app.get("/api/v1/products", response_model=List[ProductRead])
async def list_products(
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(Product)
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)
    if search:
        stmt = stmt.where(Product.title.ilike(f"%{search}%") | Product.description.ilike(f"%{search}%"))
    stmt = stmt.offset(offset).limit(limit)

    res = await db.exec(stmt)
    return res.all()


@app.get("/api/v1/products/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(Product).where(Product.id == product_id)
    res = await db.exec(stmt)
    product = res.first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


@app.post("/api/v1/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    admin_payload: dict = Depends(get_current_admin_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    product = Product(
        title=product_in.title,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        image_url=product_in.image_url,
        category_id=product_in.category_id
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@app.put("/api/v1/products/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    admin_payload: dict = Depends(get_current_admin_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(Product).where(Product.id == product_id)
    res = await db.exec(stmt)
    product = res.first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


@app.delete("/api/v1/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    admin_payload: dict = Depends(get_current_admin_user_payload),
    db: AsyncSession = Depends(get_async_session)
):
    stmt = select(Product).where(Product.id == product_id)
    res = await db.exec(stmt)
    product = res.first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    await db.delete(product)
    await db.commit()
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PRODUCT_SERVICE_PORT)
