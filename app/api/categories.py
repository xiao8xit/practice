from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud
from app.db.db import get_db
from app import schemas

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех категорий.
    
    - **skip**: количество пропускаемых записей (для пагинации)
    - **limit**: максимальное количество возвращаемых записей
    """
    categories = crud.get_categories(db=db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить категорию по ID.
    
    - **category_id**: ID категории
    """
    category = crud.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    return category


@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую категорию.
    
    - **title**: название категории (обязательно)
    """
    # Проверяем, не существует ли уже категория с таким названием
    db_category = crud.get_category_by_title(db, title=category.title)
    if db_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким названием уже существует"
        )
    
    return crud.create_category(db=db, title=category.title)


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить категорию.
    
    - **category_id**: ID обновляемой категории
    - **title**: новое название категории
    """
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Если передано новое название, проверяем уникальность
    if category_update.title is not None:
        existing_category = crud.get_category_by_title(db, title=category_update.title)
        if existing_category and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким названием уже существует"
            )
    
    updated_category = crud.update_category(
        db=db, 
        category_id=category_id, 
        title=category_update.title or db_category.title
    )
    
    if updated_category is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось обновить категорию"
        )
    
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить категорию.
    
    - **category_id**: ID удаляемой категории
    
    Примечание: все книги в этой категории также будут удалены!
    """
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    success = crud.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить категорию"
        )
    
    return None