from typing import Optional
from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    parent: Optional[int] = Field(default=None, foreign_key="categories.id", nullable=True, index=True)


class Brand(SQLModel, table=True):
    __tablename__ = "brands"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    parent: Optional[int] = Field(default=None, foreign_key="brands.id", nullable=True, index=True)


class ProductType(SQLModel, table=True):
    __tablename__ = "product_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)


class ProductAttribute(SQLModel, table=True):
    __tablename__ = "product_attributes"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    product_type: int = Field(foreign_key="product_types.id", nullable=False, index=True)
    attribute_type: str = Field(default="text", nullable=False)


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    upc: str = Field(unique=True, index=True, nullable=False)
    title: str = Field(index=True, nullable=False)
    description: str = Field(default="", nullable=False)
    type: int = Field(foreign_key="product_types.id", nullable=False, index=True)
    category: int = Field(foreign_key="categories.id", nullable=False, index=True)
    brand: Optional[int] = Field(default=None, foreign_key="brands.id", nullable=True, index=True)


class ProductAttributeValue(SQLModel, table=True):
    __tablename__ = "product_attribute_values"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_attribute: int = Field(foreign_key="product_attributes.id", nullable=False, index=True)
    value: str = Field(nullable=False)
    product: int = Field(foreign_key="products.id", nullable=False, index=True)
