from typing import Annotated, Optional, List
from pydantic import BaseModel, StringConstraints
from sqlmodel import Field

from backend.catalogue.schemas.front import (
    CategoryBase,
    BrandBase,
    ProductTypeBase,
    ProductAttributeBase,
    ProductBase
)


class CategoryCreate(CategoryBase):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    parent: Optional[int] = Field(default=None, gt=0)


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent: Optional[int] = None


class BrandCreate(BrandBase):
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    parent: Optional[int] = Field(default=None, gt=0)


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    parent: Optional[int] = None


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeUpdate(BaseModel):
    title: Optional[str] = None


class ProductAttributeCreate(ProductAttributeBase):
    pass


class ProductAttributeUpdate(BaseModel):
    name: Optional[str] = None
    product_type: Optional[int] = None
    attribute_type: Optional[str] = None


class AttributeValueInput(BaseModel):
    product_attribute: int
    value: str


class ProductCreate(ProductBase):
    attributes: Optional[List[AttributeValueInput]] = None


class ProductUpdate(BaseModel):
    upc: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[int] = None
    category: Optional[int] = None
    brand: Optional[int] = None
    attributes: Optional[List[AttributeValueInput]] = None
