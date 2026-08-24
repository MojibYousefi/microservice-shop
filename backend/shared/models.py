from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr


# ==========================================
# Database SQLModel Entities
# ==========================================

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, nullable=False)
    slug: str = Field(unique=True, index=True, nullable=False)
    description: Optional[str] = Field(default=None)


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: str = Field(default="")
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = Field(default=None)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, nullable=False)
    total_price: float = Field(gt=0)
    status: str = Field(default="pending")  # pending, paid, shipped, cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True, nullable=False)
    product_id: int = Field(nullable=False)
    product_title: str = Field(nullable=False)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


# ==========================================
# Pydantic Schemas for DTOs
# ==========================================

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    is_admin: bool = False


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool


class UserLogin(BaseModel):
    username_or_email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None


class ProductCreate(BaseModel):
    title: str
    description: str = ""
    price: float
    stock: int = 0
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ProductRead(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItem(BaseModel):
    product_id: int
    title: str
    price: float
    quantity: int
    image_url: Optional[str] = None


class CartRead(BaseModel):
    user_id: int
    items: List[CartItem]
    total_price: float


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    product_title: str
    price: float
    quantity: int


class OrderRead(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemRead] = []
