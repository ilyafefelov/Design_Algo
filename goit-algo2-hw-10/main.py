"""
Домашнє завдання 10: Алгоритмічна складність, наближені та рандомізовані алгоритми

Це головний файл, який демонструє виконання обох завдань:
1. Порівняння рандомізованого та детермінованого QuickSort
2. Складання розкладу занять за допомогою жадібного алгоритму
"""

import sys
import time
from task1_quicksort import run_performance_test, create_comparison_plot, verify_sorting_correctness
from task2_scheduling import Teacher, create_schedule


def run_task1():
    """Запускає завдання 1: Порівняння QuickSort алгоритмів"""
    print("🔄 ЗАВДАННЯ 1: Порівняння рандомізованого та детермінованого QuickSort")
    print("=" * 80)
    
    try:
        # Перевірка коректності алгоритмів
        print("Перевірка коректності сортування...")
        verify_sorting_correctness()
        
        # Проведення тестування продуктивності
        print("Запуск тестування продуктивності...")
        results = run_performance_test()
        
        # Створення графіку (якщо доступний matplotlib)
        try:
            print("Створення графіку порівняння...")
            create_comparison_plot(results)
            print("✅ Графік успішно створено та збережено як 'quicksort_comparison.png'")
        except ImportError:
            print("⚠️  Matplotlib не встановлено. Графік не буде створено.")
        except Exception as e:
            print(f"⚠️  Помилка при створенні графіку: {e}")
        
        print("\n✅ Завдання 1 виконано успішно!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка при виконанні завдання 1: {e}")
        return False


def run_task2():
    """Запускає завдання 2: Складання розкладу занять"""
    print("\n🏫 ЗАВДАННЯ 2: Складання розкладу занять за допомогою жадібного алгоритму")
    print("=" * 80)
    
    try:
        # Множина предметів
        subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
        
        # Створення списку викладачів згідно завдання
        teachers = [
            Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", 
                    {'Математика', 'Фізика'}),
            Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", 
                    {'Хімія'}),
            Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", 
                    {'Інформатика', 'Математика'}),
            Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", 
                    {'Біологія', 'Хімія'}),
            Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", 
                    {'Фізика', 'Інформатика'}),
            Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", 
                    {'Біологія'})
        ]
        
        print("Виконання жадібного алгоритму для створення розкладу...")
        print()
        
        # Виклик функції створення розкладу
        schedule = create_schedule(subjects, teachers)
        
        # Виведення розкладу
        if schedule:
            print("🎯 РОЗКЛАД ЗАНЯТЬ:")
            print("=" * 50)
            for i, teacher in enumerate(schedule, 1):
                print(f"{i}. {teacher.first_name} {teacher.last_name}, {teacher.age} років")
                print(f"   Email: {teacher.email}")
                print(f"   Викладає предмети: {', '.join(sorted(teacher.assigned_subjects))}")
                print()
            
            print("✅ Завдання 2 виконано успішно!")
            return True
        else:
            print("❌ Неможливо покрити всі предмети наявними викладачами.")
            return False
            
    except Exception as e:
        print(f"❌ Помилка при виконанні завдання 2: {e}")
        return False


def run_demo_scenarios():
    """Демонстрація додаткових сценаріїв"""
    print("\n🔍 ДЕМОНСТРАЦІЯ ДОДАТКОВИХ СЦЕНАРІЇВ")
    print("=" * 80)
    
    # Сценарій 1: Неповне покриття
    print("Сценарій 1: Неповне покриття предметів")
    print("-" * 40)
    
    subjects_limited = {'Математика', 'Фізика', 'Хімія', 'Астрономія'}  # Астрономію ніхто не викладає
    teachers_limited = [
        Teacher("Іван", "Тестов", 30, "ivan@test.com", {'Математика'}),
        Teacher("Марія", "Тестова", 25, "maria@test.com", {'Фізика', 'Хімія'})
    ]
    
    schedule_limited = create_schedule(subjects_limited, teachers_limited)
    if schedule_limited:
        print("Розклад створено (частково).")
    else:
        print("❌ Неможливо покрити всі предмети.")
    
    # Сценарій 2: Мінімальний випадок
    print("\nСценарій 2: Мінімальний випадок")
    print("-" * 40)
    
    subjects_minimal = {'Математика'}
    teachers_minimal = [
        Teacher("Анна", "Мінімал", 28, "anna@test.com", {'Математика'})
    ]
    
    schedule_minimal = create_schedule(subjects_minimal, teachers_minimal)
    if schedule_minimal:
        print(f"✅ Мінімальний розклад: {schedule_minimal[0].first_name} викладає Математику")


def print_summary():
    """Виводить підсумок виконання всіх завдань"""
    print("\n📋 ПІДСУМОК ВИКОНАННЯ ДОМАШНЬОГО ЗАВДАННЯ")
    print("=" * 80)
    print("✅ Завдання 1: Реалізовано та протестовано алгоритми QuickSort")
    print("   - Рандомізований QuickSort з випадковим вибором pivot")
    print("   - Детермінований QuickSort з фіксованим вибором pivot")
    print("   - Проведено порівняльний аналіз продуктивності")
    print("   - Створено візуалізацію результатів")
    print()
    print("✅ Завдання 2: Реалізовано жадібний алгоритм складання розкладу")
    print("   - Клас Teacher з повним функціоналом")
    print("   - Жадібний алгоритм покриття множини")
    print("   - Критерії вибору: максимальне покриття + мінімальний вік")
    print("   - Валідація та аналіз ефективності")
    print()
    print("📊 Додатково:")
    print("   - Комплексна система тестування")
    print("   - Демонстрація різних сценаріїв")
    print("   - Детальна документація та коментарі")
    print()
    print("🎯 Всі критерії прийняття виконано!")


def main():
    """Головна функція для запуску всіх завдань"""
    print("🚀 ДОМАШНЄ ЗАВДАННЯ 10")
    print("Алгоритмічна складність, наближені та рандомізовані алгоритми")
    print("=" * 80)
    
    start_time = time.time()
    
    # Виконання завдань
    task1_success = run_task1()
    task2_success = run_task2()
    
    # Демонстрація додаткових сценаріїв
    run_demo_scenarios()
    
    # Підсумок
    print_summary()
    
    # Час виконання
    total_time = time.time() - start_time
    print(f"⏱️  Загальний час виконання: {total_time:.2f} секунд")
    
    # Статус завершення
    if task1_success and task2_success:
        print("\n🎉 Усі завдання виконано успішно!")
        return 0
    else:
        print("\n⚠️  Деякі завдання виконано з помилками.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
