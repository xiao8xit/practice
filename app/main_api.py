"""
FastAPI приложение для управления библиотекой книг.
Запуск: uvicorn app.main_api:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.db import get_db, create_tables
from app.api import books, categories

# Создаем таблицы при импорте
create_tables()

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Библиотека книг API",
    description="REST API для управления библиотекой книг",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)


@app.get("/")
def read_root():
    """
    Корневой эндпоинт API.
    Возвращает информацию о API.
    """
    return {
        "message": "Добро пожаловать в API библиотеки книг!",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "categories": "/categories",
            "books": "/books",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Проверка здоровья API и подключения к базе данных.
    
    Возвращает:
    - status: "healthy" если все работает
    - database: статус подключения к БД
    """
    try:
        # Пытаемся выполнить простой запрос к БД
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "service": "books-library-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    