from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base

class Category(Base):
    """Модель категории книг"""
    __tablename__ = "categories" 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True, index=True)
    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    url = Column(String(500), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="books")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"