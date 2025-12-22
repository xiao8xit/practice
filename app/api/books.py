from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud
from app.db.db import get_db
from app import schemas

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[schemas.Book])
def read_books(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    category_id: Optional[int] = Query(None, ge=1, description="Фильтр по ID категории"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех книг с возможностью фильтрации.
    
    - **skip**: количество пропускаемых записей (для пагинации)
    - **limit**: максимальное количество возвращаемых записей
    - **category_id**: фильтр по ID категории (опционально)
    """
    books = crud.get_books(
        db=db, 
        skip=skip, 
        limit=limit,
        category_id=category_id
    )
    return books


@router.get("/{book_id}", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить книгу по ID.
    
    - **book_id**: ID книги
    """
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    return book


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую книгу.
    
    - **title**: название книги (обязательно)
    - **description**: описание книги (опционально)
    - **price**: цена книги (обязательно, должна быть > 0)
    - **url**: ссылка на книгу (опционально)
    - **category_id**: ID категории (обязательно)
    """
    # Проверяем существование категории
    category = crud.get_category(db, category_id=book.category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория с ID {book.category_id} не существует"
        )
    
    return crud.create_book(
        db=db,
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url,
        category_id=book.category_id
    )


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить книгу.
    
    - **book_id**: ID обновляемой книги
    - **title**: новое название книги (опционально)
    - **description**: новое описание книги (опционально)
    - **price**: новая цена книги (опционально)
    - **url**: новая ссылка на книгу (опционально)
    - **category_id**: новый ID категории (опционально)
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    # Проверяем существование новой категории, если она указана
    if book_update.category_id is not None:
        category = crud.get_category(db, category_id=book_update.category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категория с ID {book_update.category_id} не существует"
            )
    
    # Подготавливаем данные для обновления
    update_data = {}
    if book_update.title is not None:
        update_data['title'] = book_update.title
    if book_update.description is not None:
        update_data['description'] = book_update.description
    if book_update.price is not None:
        update_data['price'] = book_update.price
    if book_update.url is not None:
        update_data['url'] = book_update.url
    if book_update.category_id is not None:
        update_data['category_id'] = book_update.category_id
    
    updated_book = crud.update_book(db=db, book_id=book_id, **update_data)
    
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось обновить книгу"
        )
    
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить книгу.
    
    - **book_id**: ID удаляемой книги
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    success = crud.delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить книгу"
        )
    
    return None
    