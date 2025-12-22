from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import List, Optional, Dict, Any
from . import models
def create_book(
    db: Session, 
    title: str, 
    price: float, 
    category_id: int, 
    description: Optional[str] = None, 
    url: Optional[str] = None
) -> models.Book:
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    sort_by: str = "id",
    sort_order: str = "asc"
) -> List[models.Book]:
    query = db.query(models.Book)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    sort_column = getattr(models.Book, sort_by, models.Book.id)
    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    return query.offset(skip).limit(limit).all()

def update_book(
    db: Session, 
    book_id: int, 
    **kwargs
) -> Optional[models.Book]:
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in kwargs.items():
            if hasattr(db_book, key):
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book
def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False
def search_books(
    db: Session, 
    search_term: str,
    skip: int = 0,
    limit: int = 100
) -> List[models.Book]:
    return db.query(models.Book).filter(
        models.Book.title.ilike(f"%{search_term}%") | 
        models.Book.description.ilike(f"%{search_term}%")
    ).offset(skip).limit(limit).all()
def create_category(db: Session, title: str) -> models.Category:
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()
def get_category_by_title(db: Session, title: str) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.title == title).first()

def get_categories(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Category]:
    return db.query(models.Category).offset(skip).limit(limit).all()

def update_category(
    db: Session, 
    category_id: int, 
    title: str
) -> Optional[models.Category]:
    db_category = get_category(db, category_id)
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category
def delete_category(db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False
def get_books_with_category(db: Session, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    results = db.query(
        models.Book,
        models.Category.title.label("category_title")
    ).join(
        models.Category,
        models.Book.category_id == models.Category.id
    ).offset(skip).limit(limit).all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "price": book.price,
            "url": book.url,
            "category_id": book.category_id,
            "category_title": category_title
        }
        for book, category_title in results
    ]

def get_category_with_books(db: Session, category_id: int) -> Optional[Dict[str, Any]]:
    category = get_category(db, category_id)
    if not category:
        return None
    books = db.query(models.Book).filter(models.Book.category_id == category_id).all()
    return {
        "id": category.id,
        "title": category.title,
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "price": book.price
            }
            for book in books
        ]
    }