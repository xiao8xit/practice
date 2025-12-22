#!/usr/bin/env python3
"""
Скрипт для запуска FastAPI приложения.
"""

import subprocess
import sys

def run_api():
    """Запуск FastAPI приложения через uvicorn"""
    print("=" * 60)
    print("Запуск FastAPI приложения для библиотеки книг")
    print("=" * 60)
    
    print("\nДоступные команды:")
    print("1. Запустить сервер API")
    print("2. Инициализировать базу данных")
    print("3. Запустить CLI версию")
    print("4. Выйти")
    
    choice = input("\nВыберите действие (1-4): ").strip()
    
    if choice == "1":
        print("\nЗапуск API сервера...")
        print("Документация будет доступна по адресу: http://127.0.0.1:8000/docs")
        print("Нажмите Ctrl+C для остановки\n")
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    
    elif choice == "2":
        print("\nИнициализация базы данных...")
        subprocess.run([sys.executable, "-m", "app.init_db"])
    
    elif choice == "3":
        print("\nЗапуск CLI версии...")
        subprocess.run([sys.executable, "-m", "app.main_cli"])
    
    elif choice == "4":
        print("\nВыход...")
    
    else:
        print("\nНеверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    run_api()
    