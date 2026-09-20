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
from sqlmodel import select, delete
from sqlalchemy.exc import IntegrityError
from backend.gateway.security import get_current_admin_user_payload
from backend.catalogue.schemas.admin import (
    CategoryCreate,
    CategoryUpdate,
    BrandCreate,
    BrandUpdate,
    ProductTypeCreate,
    ProductTypeUpdate,
    ProductAttributeCreate,
    ProductAttributeUpdate,
    AttributeValueInput,
    ProductCreate,
    ProductUpdate
)
from backend.catalogue.schemas.front import (
    CategoryRead,
    BrandRead,
    ProductTypeRead,
    ProductAttributeRead,
    ProductAttributeValueRead,
    ProductRead
)


class CategoryAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/categories", tags=["Admin - Categories"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[CategoryRead])
        async def list_categories(
            parent_id: Optional[int] = Query(None, description="Filter by parent category ID"),
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Category]:
            stmt = select(Category)
            if parent_id is not None:
                stmt = stmt.where(Category.parent == parent_id)
            res = await db.exec(stmt)
            return list(res.all())

        @router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
        async def create_category(
            category_in: CategoryCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Category:
            if category_in.parent is not None:
                parent = await db.get(Category, category_in.parent)
                if parent is None:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Parent category not found."
                    )

            category = Category(
                name=category_in.name,
                parent=category_in.parent
            )
            db.add(category)
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category could not be created. Check the parent category and submitted data."
                ) from None
            await db.refresh(category)
            return category

        @router.put("/{category_id}", response_model=CategoryRead)
        async def update_category(
            category_id: int,
            category_in: CategoryUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Category:
            stmt = select(Category).where(Category.id == category_id)
            res = await db.exec(stmt)
            category = res.first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

            update_data = category_in.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(category, k, v)

            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category

        @router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_category(
            category_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(Category).where(Category.id == category_id)
            res = await db.exec(stmt)
            category = res.first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")

            children = await db.exec(select(Category.id).where(Category.parent == category_id).limit(1))
            if children.first() is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This category has subcategories. Delete or move them before deleting it."
                )

            products = await db.exec(select(Product.id).where(Product.category == category_id).limit(1))
            if products.first() is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This category has products. Delete or move them before deleting it."
                )

            try:
                await db.delete(category)
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This category is referenced by other data and cannot be deleted. Remove or move its references first."
                ) from None
            return None

        return router


class BrandAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/brands", tags=["Admin - Brands"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.get("", response_model=List[BrandRead])
        async def list_brands(
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> List[Brand]:
            stmt = select(Brand)
            res = await db.exec(stmt)
            return list(res.all())

        @router.post("", response_model=BrandRead, status_code=status.HTTP_201_CREATED)
        async def create_brand(
            brand_in: BrandCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Brand:
            if brand_in.parent is not None:
                parent = await db.get(Brand, brand_in.parent)
                if parent is None:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Parent brand not found."
                    )

            brand = Brand(
                name=brand_in.name,
                parent=brand_in.parent
            )
            db.add(brand)
            try:
                await db.commit()
            except IntegrityError:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Brand could not be created. Check the parent brand and submitted data."
                ) from None
            await db.refresh(brand)
            return brand

        @router.put("/{brand_id}", response_model=BrandRead)
        async def update_brand(
            brand_id: int,
            brand_in: BrandUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Brand:
            stmt = select(Brand).where(Brand.id == brand_id)
            res = await db.exec(stmt)
            brand = res.first()
            if not brand:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found.")

            update_data = brand_in.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(brand, k, v)

            db.add(brand)
            await db.commit()
            await db.refresh(brand)
            return brand

        @router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_brand(
            brand_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(Brand).where(Brand.id == brand_id)
            res = await db.exec(stmt)
            brand = res.first()
            if not brand:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found.")

            await db.delete(brand)
            await db.commit()
            return None

        return router


class ProductTypeAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/types", tags=["Admin - Types & Attributes"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.post("", response_model=ProductTypeRead, status_code=status.HTTP_201_CREATED)
        async def create_type(
            type_in: ProductTypeCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductType:
            ptype = ProductType(title=type_in.title)
            db.add(ptype)
            await db.commit()
            await db.refresh(ptype)
            return ptype

        @router.put("/{type_id}", response_model=ProductTypeRead)
        async def update_type(
            type_id: int,
            type_in: ProductTypeUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductType:
            stmt = select(ProductType).where(ProductType.id == type_id)
            res = await db.exec(stmt)
            ptype = res.first()
            if not ptype:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found.")

            if type_in.title is not None:
                ptype.title = type_in.title

            db.add(ptype)
            await db.commit()
            await db.refresh(ptype)
            return ptype

        @router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_type(
            type_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(ProductType).where(ProductType.id == type_id)
            res = await db.exec(stmt)
            ptype = res.first()
            if not ptype:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ProductType not found.")

            await db.delete(ptype)
            await db.commit()
            return None

        @router.post("/attributes", response_model=ProductAttributeRead, status_code=status.HTTP_201_CREATED)
        async def create_attribute(
            attr_in: ProductAttributeCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductAttribute:
            attr = ProductAttribute(
                name=attr_in.name,
                product_type=attr_in.product_type,
                attribute_type=attr_in.attribute_type
            )
            db.add(attr)
            await db.commit()
            await db.refresh(attr)
            return attr

        @router.put("/attributes/{attribute_id}", response_model=ProductAttributeRead)
        async def update_attribute(
            attribute_id: int,
            attr_in: ProductAttributeUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductAttribute:
            stmt = select(ProductAttribute).where(ProductAttribute.id == attribute_id)
            res = await db.exec(stmt)
            attr = res.first()
            if not attr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found.")

            update_data = attr_in.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(attr, k, v)

            db.add(attr)
            await db.commit()
            await db.refresh(attr)
            return attr

        @router.delete("/attributes/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_attribute(
            attribute_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(ProductAttribute).where(ProductAttribute.id == attribute_id)
            res = await db.exec(stmt)
            attr = res.first()
            if not attr:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attribute not found.")

            await db.delete(attr)
            await db.commit()
            return None

        return router


class ProductAdminView:
    router = APIRouter(prefix="/api/v1/catalogue/admin/products", tags=["Admin - Products"])

    @classmethod
    def register_routes(cls) -> APIRouter:
        router = cls.router

        @router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
        async def create_product(
            product_in: ProductCreate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Product:
            # Check unique UPC
            upc_stmt = select(Product).where(Product.upc == product_in.upc)
            upc_res = await db.exec(upc_stmt)
            if upc_res.first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UPC already registered.")

            product = Product(
                upc=product_in.upc,
                title=product_in.title,
                description=product_in.description,
                type=product_in.type,
                category=product_in.category,
                brand=product_in.brand
            )
            db.add(product)
            await db.commit()
            await db.refresh(product)

            # Add optional initial attribute values
            if product_in.attributes:
                for attr_val in product_in.attributes:
                    val_obj = ProductAttributeValue(
                        product_attribute=attr_val.product_attribute,
                        value=attr_val.value,
                        product=product.id  # type: ignore
                    )
                    db.add(val_obj)
                await db.commit()

            return product

        @router.put("/{product_id}", response_model=ProductRead)
        async def update_product(
            product_id: int,
            product_in: ProductUpdate,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> Product:
            stmt = select(Product).where(Product.id == product_id)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            update_data = product_in.model_dump(exclude_unset=True)
            attributes_data = update_data.pop("attributes", None)

            for k, v in update_data.items():
                setattr(product, k, v)

            db.add(product)
            await db.commit()
            await db.refresh(product)

            # Sync attribute values if specified
            if attributes_data is not None:
                # Delete existing values
                del_stmt = delete(ProductAttributeValue).where(ProductAttributeValue.product == product.id)
                await db.exec(del_stmt)
                for attr_val in attributes_data:
                    val_obj = ProductAttributeValue(
                        product_attribute=attr_val["product_attribute"],
                        value=attr_val["value"],
                        product=product.id  # type: ignore
                    )
                    db.add(val_obj)
                await db.commit()

            return product

        @router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_product(
            product_id: int,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> None:
            stmt = select(Product).where(Product.id == product_id)
            res = await db.exec(stmt)
            product = res.first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            # Delete attribute values
            del_stmt = delete(ProductAttributeValue).where(ProductAttributeValue.product == product.id)
            await db.exec(del_stmt)

            await db.delete(product)
            await db.commit()
            return None

        @router.post("/{product_id}/attributes", response_model=ProductAttributeValueRead, status_code=status.HTTP_201_CREATED)
        async def set_product_attribute_value(
            product_id: int,
            val_in: AttributeValueInput,
            admin_user: Dict[str, Any] = Depends(get_current_admin_user_payload),
            db: AsyncSession = Depends(get_async_session)
        ) -> ProductAttributeValueRead:
            prod_stmt = select(Product).where(Product.id == product_id)
            prod_res = await db.exec(prod_stmt)
            if not prod_res.first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

            # Check if attribute already exists for product -> update, else insert
            val_stmt = select(ProductAttributeValue).where(
                ProductAttributeValue.product == product_id,
                ProductAttributeValue.product_attribute == val_in.product_attribute
            )
            val_res = await db.exec(val_stmt)
            existing_val = val_res.first()

            if existing_val:
                existing_val.value = val_in.value
                db.add(existing_val)
                await db.commit()
                await db.refresh(existing_val)
                res_obj = existing_val
            else:
                new_val = ProductAttributeValue(
                    product_attribute=val_in.product_attribute,
                    value=val_in.value,
                    product=product_id
                )
                db.add(new_val)
                await db.commit()
                await db.refresh(new_val)
                res_obj = new_val

            attr_def_stmt = select(ProductAttribute).where(ProductAttribute.id == res_obj.product_attribute)
            attr_def_res = await db.exec(attr_def_stmt)
            attr_def = attr_def_res.first()

            return ProductAttributeValueRead(
                id=res_obj.id,  # type: ignore
                product_attribute=res_obj.product_attribute,
                attribute_name=attr_def.name if attr_def else None,
                value=res_obj.value,
                product=res_obj.product
            )

        return router
