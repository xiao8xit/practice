import sqlalchemy as sa
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from . import models


# ========== CRUD для категорий (Category) ==========
def create_category(db: Session, title: str) -> models.Category:
    """Создание новой категории"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """Получение категории по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_title(db: Session, title: str) -> Optional[models.Category]:
    """Получение категории по названию"""
    return db.query(models.Category).filter(models.Category.title == title).first()


def get_categories(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    sort_by: str = "id",
    sort_order: str = "asc"
) -> List[models.Category]:
    """Получение списка категорий с сортировкой"""
    query = db.query(models.Category)
    
    # Сортировка
    sort_column = getattr(models.Category, sort_by, models.Category.id)
    if sort_order.lower() == "desc":
        query = query.order_by(sa.desc(sort_column))
    else:
        query = query.order_by(sa.asc(sort_column))
    
    return query.offset(skip).limit(limit).all()


def update_category(
    db: Session, 
    category_id: int, 
    title: str
) -> Optional[models.Category]:
    """Обновление категории"""
    db_category = get_category(db, category_id)
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> bool:
    """Удаление категории (вместе со всеми связанными книгами)"""
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False


# ========== CRUD для книг (Book) ==========
def create_book(
    db: Session, 
    title: str, 
    price: float, 
    category_id: int, 
    description: Optional[str] = None, 
    url: Optional[str] = None
) -> models.Book:
    """Создание новой книги"""
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
    """Получение книги по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    sort_by: str = "id",
    sort_order: str = "asc"
) -> List[models.Book]:
    """Получение списка книг с фильтрацией и сортировкой"""
    query = db.query(models.Book)
    
    # Фильтрация по категории
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    
    # Сортировка
    sort_column = getattr(models.Book, sort_by, models.Book.id)
    if sort_order.lower() == "desc":
        query = query.order_by(sa.desc(sort_column))
    else:
        query = query.order_by(sa.asc(sort_column))
    
    return query.offset(skip).limit(limit).all()


def get_book_with_category(db: Session, book_id: int) -> Optional[models.Book]:
    """Получение книги с информацией о категории"""
    return db.query(models.Book).options(
        sa.orm.joinedload(models.Book.category)
    ).filter(models.Book.id == book_id).first()


def get_books_with_category(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None
) -> List[models.Book]:
    """Получение списка книг с информацией о категории"""
    query = db.query(models.Book).options(
        sa.orm.joinedload(models.Book.category)
    )
    
    # Фильтрация по категории
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    
    return query.offset(skip).limit(limit).all()


def update_book(
    db: Session, 
    book_id: int, 
    **kwargs
) -> Optional[models.Book]:
    """Обновление книги"""
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in kwargs.items():
            if value is not None and hasattr(db_book, key):
                setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    """Удаление книги"""
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
    """Поиск книг по названию или описанию"""
    return db.query(models.Book).filter(
        models.Book.title.ilike(f"%{search_term}%") | 
        models.Book.description.ilike(f"%{search_term}%")
    ).offset(skip).limit(limit).all()


def get_books_count_by_category(db: Session) -> Dict[int, int]:
    """Получение количества книг по категориям"""
    result = db.query(
        models.Book.category_id,
        sa.func.count(models.Book.id).label('count')
    ).group_by(models.Book.category_id).all()
    
    return {category_id: count for category_id, count in result}


def get_category_with_books(db: Session, category_id: int) -> Optional[models.Category]:
    """Получение категории со всеми книгами"""
    return db.query(models.Category).options(
        sa.orm.joinedload(models.Category.books)
    ).filter(models.Category.id == category_id).first()