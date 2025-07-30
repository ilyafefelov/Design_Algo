"""
Main script to run both tasks for Homework 7
"""

import sys
import os
from task1 import main as task1_main
from task2 import main as task2_main


def run_task1():
    """Run Task 1: LRU Cache optimization"""
    print("🚀 Запуск Завдання 1")
    print()
    try:
        task1_main()
        print("✅ Завдання 1 успішно виконано!")
        return True
    except Exception as e:
        print(f"❌ Помилка в Завданні 1: {e}")
        return False


def run_task2():
    """Run Task 2: Fibonacci comparison"""
    print("\n" + "="*80)
    print("🚀 Запуск Завдання 2")
    print()
    try:
        task2_main()
        print("✅ Завдання 2 успішно виконано!")
        return True
    except Exception as e:
        print(f"❌ Помилка в Завданні 2: {e}")
        return False


def main():
    """Main function to run both tasks"""
    print("Домашнє завдання 7: Алгоритми керування кешем")
    print("="*80)
    print("Виконання двох завдань:")
    print("1. Оптимізація доступу до даних за допомогою LRU-кешу")
    print("2. Порівняння продуктивності обчислення чисел Фібоначчі")
    print("="*80)
    
    # Track success
    task1_success = False
    task2_success = False
    
    # Run Task 1
    task1_success = run_task1()
    
    # Run Task 2 only if Task 1 succeeded or user wants to continue
    if task1_success:
        task2_success = run_task2()
    else:
        print("\nБажаєте все одно виконати Завдання 2? (y/n): ", end="")
        choice = input().lower().strip()
        if choice in ['y', 'yes', 'так', 'т']:
            task2_success = run_task2()
    
    # Final summary
    print("\n" + "="*80)
    print("ПІДСУМОК ВИКОНАННЯ")
    print("="*80)
    print(f"Завдання 1 (LRU Cache): {'✅ Виконано' if task1_success else '❌ Помилка'}")
    print(f"Завдання 2 (Fibonacci): {'✅ Виконано' if task2_success else '❌ Помилка'}")
    
    if task1_success and task2_success:
        print("\n🎉 Всі завдання успішно виконані!")
        print("\nФайли створені:")
        print("- fibonacci_comparison.png (графік порівняння)")
        print("- Всі модулі та тести")
    elif task1_success or task2_success:
        print("\n⚠️  Частково виконано. Перевірте помилки вище.")
    else:
        print("\n💥 Помилки в обох завданнях. Перевірте налаштування.")
    
    print("\nДля запуску окремих завдань використовуйте:")
    print("- python task1.py")
    print("- python task2.py")
    print("\nДля запуску тестів:")
    print("- python test_task1.py")
    print("- python test_task2.py")


if __name__ == "__main__":
    main()
