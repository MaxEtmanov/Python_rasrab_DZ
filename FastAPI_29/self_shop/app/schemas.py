from pydantic import BaseModel, Field, validator
from typing import List, Optional

# Схема для товара
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Название товара не может быть пустым")
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Цена товара должна быть больше 0")
    category_id: Optional[int] = None
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Название товара не может быть пустым')
        return v
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Цена товара должна быть больше 0')
        return v

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = None

    class Config:
        orm_mode = True

# Схема для категории
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Схема для пользователя
class UserCreate(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """    
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Схема для заказа
class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]
    total_price: float

    class Config:
        orm_mode = True