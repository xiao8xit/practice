
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import SessionLocal, create_tables, engine
from app.db import crud, models
def init_database():
    print("=" * 60)
    print("Инициализация базы данных...")
    print("=" * 60)
    create_tables()
    print("✓ Таблицы созданы")
    db = SessionLocal()
    try:
        existing_categories = crud.get_categories(db)
        if existing_categories:
            print("В базе уже есть данные. Хотите пересоздать? (y/n)")
            response = input().lower()
            if response != 'y':
                print("Инициализация отменена")
                return
        db.query(models.Book).delete()
        db.query(models.Category).delete()
        db.commit()
        print("✓ Существующие данные удалены")
        categories_data = [
            {
                "title": "Фантастика",
                "books": [
                    {
                        "title": "Властелин колец",
                        "description": "Эпическая фэнтези-сага о Средиземье",
                        "price": 799.99,
                        "url": "https://example.com/lotr"
                    },
                    {
                        "title": "1984",
                        "description": "Антиутопический роман Джорджа Оруэлла",
                        "price": 450.50,
                        "url": "https://example.com/1984"
                    },
                    {
                        "title": "Марсианин",
                        "description": "Научно-фантастический роман о выживании на Марсе",
                        "price": 550.00,
                        "url": "https://example.com/martian"
                    }
                ]
            },
            {
                "title": "Программирование",
                "books": [
                    {
                        "title": "Чистый код",
                        "description": "Создание, анализ и рефакторинг кода",
                        "price": 1200.00,
                        "url": "https://example.com/clean-code"
                    },
                    {
                        "title": "Грокаем алгоритмы",
                        "description": "Иллюстрированное пособие для программистов",
                        "price": 850.75,
                        "url": "https://example.com/grokking-algorithms"
                    },
                    {
                        "title": "Python. К вершинам мастерства",
                        "description": "Продвинутое программирование на Python",
                        "price": 950.00,
                        "url": "https://example.com/python-mastery"
                    },
                    {
                        "title": "SQL для простых смертных",
                        "description": "Полное руководство по SQL для начинающих",
                        "price": 700.25,
                        "url": "https://example.com/sql-guide"
                    }
                ]
            }
        ]
        
        print("\nДобавление категорий и книг...")
        print("-" * 60)
        for category_info in categories_data:
            category = crud.create_category(db, title=category_info["title"])
            print(f"✓ Категория создана: {category.title}")
            for book_info in category_info["books"]:
                book = crud.create_book(
                    db=db,
                    title=book_info["title"],
                    description=book_info["description"],
                    price=book_info["price"],
                    url=book_info["url"],
                    category_id=category.id
                )
                print(f"  • Книга добавлена: {book.title} ({book.price} руб.)")
        print("-" * 60)
        print("✓ Инициализация завершена успешно!")
        print("=" * 60)
        categories_count = len(crud.get_categories(db))
        books_count = len(crud.get_books(db))
        print(f"\nСтатистика:")
        print(f"Категорий: {categories_count}")
        print(f"Книг: {books_count}")
    except Exception as e:
        print(f"Ошибка при инициализации: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()