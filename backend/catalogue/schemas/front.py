from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str
    parent: Optional[int] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoryTreeRead(CategoryRead):
    children: List["CategoryTreeRead"] = []


class BrandBase(BaseModel):
    name: str
    parent: Optional[int] = None


class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductTypeBase(BaseModel):
    title: str


class ProductTypeRead(ProductTypeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductAttributeBase(BaseModel):
    name: str
    product_type: int
    attribute_type: str = "text"


class ProductAttributeRead(ProductAttributeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductAttributeValueRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_attribute: int
    attribute_name: Optional[str] = None
    value: str
    product: int


class ProductBase(BaseModel):
    upc: str
    title: str
    description: str = ""
    type: int
    category: int
    brand: Optional[int] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductDetailRead(ProductRead):
    category_name: Optional[str] = None
    brand_name: Optional[str] = None
    type_title: Optional[str] = None
    attributes: List[ProductAttributeValueRead] = []
