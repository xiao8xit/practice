from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


# ========== Category Schemas ==========
class CategoryBase(BaseModel):
    """Базовая схема для категории"""
    title: str = Field(..., min_length=1, max_length=255, description="Название категории")


class CategoryCreate(CategoryBase):
    """Схема для создания категории"""
    pass


class CategoryUpdate(BaseModel):
    """Схема для обновления категории"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Название категории")


class Category(CategoryBase):
    """Схема ответа для категории"""
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ========== Book Schemas ==========
class BookBase(BaseModel):
    """Базовая схема для книги"""
    title: str = Field(..., min_length=1, max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: float = Field(..., gt=0, description="Цена книги (должна быть больше 0)")
    url: Optional[str] = Field(None, max_length=500, description="Ссылка на книгу")
    category_id: int = Field(..., ge=1, description="ID категории")


class BookCreate(BookBase):
    """Схема для создания книги"""
    pass


class BookUpdate(BaseModel):
    """Схема для обновления книги"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    price: Optional[float] = Field(None, gt=0, description="Цена книги")
    url: Optional[str] = Field(None, max_length=500, description="Ссылка на книгу")
    category_id: Optional[int] = Field(None, ge=1, description="ID категории")


class Book(BookBase):
    """Схема ответа для книги"""
    id: int
    created_at: datetime
    category: Optional[Category] = None
    model_config = ConfigDict(from_attributes=True)


class BookWithCategory(Book):
    """Схема книги с полной информацией о категории"""
    pass