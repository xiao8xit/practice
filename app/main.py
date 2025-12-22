
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.db import SessionLocal
from app.db import crud
def display_categories(db):
    """Отображение категорий"""
    print("\n" + "=" * 80)
    print("КАТЕГОРИИ КНИГ")
    print("=" * 80)
    
    categories = crud.get_categories(db)
    
    if not categories:
        print("Нет категорий в базе данных")
        return
    
    for i, category in enumerate(categories, 1):
        print(f"\n{i}. {category.title.upper()}")
        print("-" * 40)

        books = crud.get_books(db, category_id=category.id)
        
        if books:
            for j, book in enumerate(books, 1):
                print(f"   {j:2}. {book.title}")
                print(f"       Описание: {book.description[:80]}..." if book.description and len(book.description) > 80 else 
                      f"       Описание: {book.description or 'Нет описания'}")
                print(f"       Цена: {book.price:8.2f} руб.")
                print(f"       Ссылка: {book.url or 'Нет ссылки'}")
                print()
        else:
            print("   Нет книг в этой категории")

def display_books_with_categories(db):
    print("\n" + "=" * 80)
    print("ВСЕ КНИГИ С КАТЕГОРИЯМИ")
    print("=" * 80)
    
    books_with_categories = crud.get_books_with_category(db)
    
    if not books_with_categories:
        print("Нет книг в базе данных")
        return
    
    for i, book_info in enumerate(books_with_categories, 1):
        print(f"\n{i:2}. {book_info['title']}")
        print(f"    Категория: {book_info['category_title']}")
        print(f"    Описание: {book_info['description'][:100]}..." if book_info['description'] and len(book_info['description']) > 100 else 
              f"    Описание: {book_info['description'] or 'Нет описания'}")
        print(f"    Цена: {book_info['price']:8.2f} руб.")
        print(f"    Ссылка: {book_info['url'] or 'Нет ссылки'}")

def display_statistics(db):
    print("\n" + "=" * 80)
    print("СТАТИСТИКА БИБЛИОТЕКИ")
    print("=" * 80)
    
    categories = crud.get_categories(db)
    books = crud.get_books(db)
    
    print(f"\nОбщее количество категорий: {len(categories)}")
    print(f"Общее количество книг: {len(books)}")
    
    if categories and books:
        total_price = sum(book.price for book in books)
        avg_price = total_price / len(books) if books else 0
        
        print(f"Средняя цена книги: {avg_price:.2f} руб.")
        print(f"Общая стоимость всех книг: {total_price:.2f} руб.")
        
        print("\nКниг по категориям:")
        print("-" * 40)
        
        for category in categories:
            category_books = crud.get_books(db, category_id=category.id)
            category_total = sum(book.price for book in category_books)
            print(f"{category.title}: {len(category_books)} книг, общая стоимость: {category_total:.2f} руб.")

def search_books_interactive(db):
    print("\n" + "=" * 80)
    print("ПОИСК КНИГ")
    print("=" * 80)
    
    search_term = input("\nВведите поисковый запрос: ").strip()
    
    if not search_term:
        print("Поисковый запрос не может быть пустым")
        return
    
    results = crud.search_books(db, search_term=search_term)
    
    if results:
        print(f"\nНайдено {len(results)} книг по запросу '{search_term}':")
        print("-" * 60)
        
        for i, book in enumerate(results, 1):
            category = crud.get_category(db, book.category_id)
            category_name = category.title if category else "Неизвестно"
            
            print(f"\n{i:2}. {book.title}")
            print(f"    Категория: {category_name}")
            print(f"    Описание: {book.description[:80]}..." if book.description and len(book.description) > 80 else 
                  f"    Описание: {book.description or 'Нет описания'}")
            print(f"    Цена: {book.price:8.2f} руб.")
    else:
        print(f"\nПо запросу '{search_term}' ничего не найдено")

def main():
    print("\n" + "=" * 80)
    print("БИБЛИОТЕКА КНИГ - ГЛАВНОЕ МЕНЮ")
    print("=" * 80)

    db = SessionLocal()
    
    try:
        while True:
            print("\nВыберите действие:")
            print("1. Показать все категории с книгами")
            print("2. Показать все книги с категориями")
            print("3. Показать статистику библиотеки")
            print("4. Поиск книг")
            print("5. Выйти")
            
            choice = input("\nВаш выбор (1-5): ").strip()
            
            if choice == "1":
                display_categories(db)
            elif choice == "2":
                display_books_with_categories(db)
            elif choice == "3":
                display_statistics(db)
            elif choice == "4":
                search_books_interactive(db)
            elif choice == "5":
                print("\nВыход из программы...")
                break
            else:
                print("\nНеверный выбор. Попробуйте снова.")
                
            input("\nНажмите Enter для продолжения...")
            
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
    finally:
        db.close()
        print("\nСессия базы данных закрыта")

if __name__ == "__main__":
    main()