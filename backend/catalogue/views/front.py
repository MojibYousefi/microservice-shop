from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.config.database import get_async_session
from backend.catalogue.models import (
    Category,
    Brand,
    ProductType,
    ProductAttribute,
    Product,
    ProductAttributeValue
)
from sqlmodel import select
from backend.catalogue.schemas.front import (
    CategoryRead,
    CategoryTreeRead,
    BrandRead,
    ProductTypeRead,
    ProductAttributeRead,
    ProductAttributeValueRead,
    ProductRead,
    ProductDetailRead
)


class CategoryFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/categories", tags=["Front - Categories"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[CategoryRead])
        async def list_categories(
            parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Category]:
            stmt = select(Category)
            if parent_id is not None:
                stmt = stmt.where(Category.parent == parent_id)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/tree", response_model=List[CategoryTreeRead])
        async def get_category_tree(
            db: AsyncSession = Depends(get_async_session)
        ) -> List[CategoryTreeRead]:
            stmt = select(Category)
            res = await db.exec(stmt)
            all_categories = list(res.all())

            # Build recursive hierarchy
            category_map: Dict[int, CategoryTreeRead] = {
                c.id: CategoryTreeRead(id=c.id, name=c.name, parent=c.parent, children=[])  # type: ignore
                for c in all_categories if c.id is not None
            }

            tree: List[CategoryTreeRead] = []
            for c in all_categories:
                if c.id is not None:
                    node = category_map[c.id]
                    if c.parent and c.parent in category_map:
                        category_map[c.parent].children.append(node)
                    else:
                        tree.append(node)
            return tree

        @router.get("/{category_id}", response_model=CategoryRead)
        async def get_category(
            category_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> Category:
            stmt = select(Category).where(Category.id == category_id)
            res = await db.exec(stmt)
            category = res.first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
            return category

        return router


class BrandFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/brands", tags=["Front - Brands"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[BrandRead])
        async def list_brands(
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Brand]:
            stmt = select(Brand)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/{brand_id}", response_model=BrandRead)
        async def get_brand(
            brand_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> Brand:
            stmt = select(Brand).where(Brand.id == brand_id)
            res = await db.exec(stmt)
            brand = res.first()
            if not brand:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found.")
            return brand

        return router


class ProductTypeFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/types", tags=["Front - Product Types"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[ProductTypeRead])
        async def list_types(
            db: AsyncSession = Depends(get_async_session)
        ) -> List[ProductType]:
            stmt = select(ProductType)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/{type_id}/attributes", response_model=List[ProductAttributeRead])
        async def list_type_attributes(
            type_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> List[ProductAttribute]:
            stmt = select(ProductAttribute).where(ProductAttribute.product_type == type_id)
            res = await db.exec(stmt)
            return list(res.all())

        return router


class ProductFrontView:
    router = APIRouter(prefix="/api/v1/catalogue/products", tags=["Front - Products"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[ProductRead])
        async def list_products(
            search: Optional[str] = Query(None, description="Search by title or description"),
            category_id: Optional[int] = Query(None, description="Filter by category"),
            brand_id: Optional[int] = Query(None, description="Filter by brand"),
            type_id: Optional[int] = Query(None, description="Filter by product type"),
            limit: int = Query(50, ge=1, le=100),
            offset: int = Query(0, ge=0),
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Product]:
            stmt = select(Product)
            if search:
                stmt = stmt.where(Product.title.ilike(f"%{search}%") | Product.description.ilike(f"%{search}%"))
            if category_id is not None:
                stmt = stmt.where(Product.category == category_id)
            if brand_id is not None:
                stmt = stmt.where(Product.brand == brand_id)
            if type_id is not None:
                stmt = stmt.where(Product.type == type_id)

            stmt = stmt.offset(offset).limit(limit)
            res = await db.exec(stmt)
            return list(res.all())

        @router.get("/{product_id}", response_model=ProductDetailRead)
        async def get_product_detail(
            product_id: int,
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductDetailRead:
            stmt = select(Product).where(Product.id == product_id)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            # Resolve Category, Brand, and Type Names
            cat_stmt = select(Category).where(Category.id == product.category)
            cat_res = await db.exec(cat_stmt)
            cat = cat_res.first()

            brand_name = None
            if product.brand:
                brand_stmt = select(Brand).where(Brand.id == product.brand)
                brand_res = await db.exec(brand_stmt)
                b = brand_res.first()
                if b:
                    brand_name = b.name

            type_stmt = select(ProductType).where(ProductType.id == product.type)
            type_res = await db.exec(type_stmt)
            ptype = type_res.first()

            # Resolve Attributes
            val_stmt = select(ProductAttributeValue).where(ProductAttributeValue.product == product.id)
            val_res = await db.exec(val_stmt)
            attr_values = list(val_res.all())

            attr_items: List[ProductAttributeValueRead] = []
            for val in attr_values:
                attr_def_stmt = select(ProductAttribute).where(ProductAttribute.id == val.product_attribute)
                attr_def_res = await db.exec(attr_def_stmt)
                attr_def = attr_def_res.first()
                attr_items.append(ProductAttributeValueRead(
                    id=val.id,  # type: ignore
                    product_attribute=val.product_attribute,
                    attribute_name=attr_def.name if attr_def else None,
                    value=val.value,
                    product=val.product
                ))

            return ProductDetailRead(
                id=product.id,  # type: ignore
                upc=product.upc,
                title=product.title,
                description=product.description,
                type=product.type,
                category=product.category,
                brand=product.brand,
                category_name=cat.name if cat else None,
                brand_name=brand_name,
                type_title=ptype.title if ptype else None,
                attributes=attr_items
            )

        @router.get("/upc/{upc_code}", response_model=ProductDetailRead)
        async def get_product_by_upc(
            upc_code: str,
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductDetailRead:
            stmt = select(Product).where(Product.upc == upc_code)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
            return await get_product_detail(product.id, db)  # type: ignore

        return router
