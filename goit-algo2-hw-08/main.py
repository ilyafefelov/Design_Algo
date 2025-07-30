"""
Main script to run both tasks for Homework 8

This script demonstrates both rate limiting algorithms:
1. Sliding Window Rate Limiter
2. Throttling Rate Limiter
"""

import sys
import time
from task1 import test_rate_limiter as test_sliding_window
from task2 import test_throttling_limiter


def run_task1():
    """Run Task 1: Sliding Window Rate Limiter"""
    print("🚀 Запуск Завдання 1: Sliding Window Rate Limiter")
    print("=" * 60)
    try:
        test_sliding_window()
        print("✅ Завдання 1 успішно виконано!")
        return True
    except Exception as e:
        print(f"❌ Помилка в Завданні 1: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_task2():
    """Run Task 2: Throttling Rate Limiter"""
    print("\n" + "🚀 Запуск Завдання 2: Throttling Rate Limiter")
    print("=" * 60)
    try:
        test_throttling_limiter()
        print("✅ Завдання 2 успішно виконано!")
        return True
    except Exception as e:
        print(f"❌ Помилка в Завданні 2: {e}")
        import traceback
        traceback.print_exc()
        return False


def compare_algorithms():
    """Compare both algorithms side by side"""
    print("\n" + "🔄 Порівняння алгоритмів")
    print("=" * 60)
    
    print("\n📊 ХАРАКТЕРИСТИКИ АЛГОРИТМІВ:")
    print("=" * 40)
    
    print("SLIDING WINDOW:")
    print("✓ Точний контроль кількості запитів у часовому вікні")
    print("✓ Дозволяє пакетні запити до досягнення ліміту")
    print("✓ Автоматичне очищення застарілих записів")
    print("✓ Складність пам'яті: O(n) де n - кількість запитів у вікні")
    print("✓ Складність часу: O(1) амортизована для операцій")
    
    print("\nTHROTTLING:")
    print("✓ Фіксований інтервал між запитами")
    print("✓ Простіша реалізація та менше пам'яті")
    print("✓ Гарантований мінімальний інтервал")
    print("✓ Складність пам'яті: O(1) на користувача")
    print("✓ Складність часу: O(1) для всіх операцій")
    
    print("\n🎯 КОЛИ ВИКОРИСТОВУВАТИ:")
    print("=" * 30)
    
    print("SLIDING WINDOW - коли потрібно:")
    print("• Точний контроль кількості запитів")
    print("• Дозволити 'пакети' запитів")
    print("• Справедливий розподіл ресурсів")
    print("• API rate limiting з точними лімітами")
    
    print("\nTHROTTLING - коли потрібно:")
    print("• Рівномірний розподіл навантаження")
    print("• Запобігання спаму в чатах")
    print("• Контроль частоти повідомлень")
    print("• Менше використання пам'яті")
    
    # Practical demonstration
    print("\n🧪 ПРАКТИЧНА ДЕМОНСТРАЦІЯ РІЗНИЦІ:")
    print("=" * 45)
    
    from task1 import SlidingWindowRateLimiter
    from task2 import ThrottlingRateLimiter
    
    # Create both limiters with equivalent settings
    sliding = SlidingWindowRateLimiter(window_size=10, max_requests=1)
    throttling = ThrottlingRateLimiter(min_interval=10.0)
    
    print("\nСценарій: Користувач надсилає 3 повідомлення підряд")
    
    # Test scenario: 3 rapid messages
    print("\nSLIDING WINDOW результати:")
    for i in range(3):
        result = sliding.record_message("demo_user")
        wait_time = sliding.time_until_next_allowed("demo_user")
        print(f"  Повідомлення {i+1}: {'✓' if result else '×'} "
              f"(очікування: {wait_time:.1f}с)")
        time.sleep(0.1)  # Small delay
    
    print("\nTHROTTLING результати:")
    for i in range(3):
        result = throttling.record_message("demo_user")
        wait_time = throttling.time_until_next_allowed("demo_user")
        print(f"  Повідомлення {i+1}: {'✓' if result else '×'} "
              f"(очікування: {wait_time:.1f}с)")
        time.sleep(0.1)  # Small delay


def run_tests():
    """Run unit tests for both tasks"""
    print("\n" + "🧪 Запуск тестів")
    print("=" * 30)
    
    import subprocess
    import os
    
    try:
        print("Тестування Task 1...")
        result1 = subprocess.run([
            sys.executable, "test_task1.py"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result1.returncode == 0:
            print("✅ Тести Task 1 пройшли успішно")
        else:
            print("❌ Помилки в тестах Task 1:")
            print(result1.stderr)
        
        print("\nТестування Task 2...")
        result2 = subprocess.run([
            sys.executable, "test_task2.py"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result2.returncode == 0:
            print("✅ Тести Task 2 пройшли успішно")
        else:
            print("❌ Помилки в тестах Task 2:")
            print(result2.stderr)
            
        return result1.returncode == 0 and result2.returncode == 0
        
    except Exception as e:
        print(f"❌ Помилка при запуску тестів: {e}")
        return False


def interactive_demo():
    """Interactive demonstration of both algorithms"""
    print("\n" + "🎮 Інтерактивна демонстрація")
    print("=" * 40)
    
    from task1 import SlidingWindowRateLimiter
    from task2 import ThrottlingRateLimiter
    
    sliding = SlidingWindowRateLimiter(window_size=5, max_requests=2)
    throttling = ThrottlingRateLimiter(min_interval=3.0)
    
    print("Налаштування для демонстрації:")
    print("• Sliding Window: 5 секунд, максимум 2 повідомлення")
    print("• Throttling: 3 секунди між повідомленнями")
    print("\nВведіть ID користувача (або 'quit' для виходу):")
    
    try:
        while True:
            user_input = input("\nКористувач ID: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            # Test both algorithms
            sliding_result = sliding.record_message(user_input)
            sliding_wait = sliding.time_until_next_allowed(user_input)
            
            throttling_result = throttling.record_message(user_input)
            throttling_wait = throttling.time_until_next_allowed(user_input)
            
            print(f"\nРезультати для користувача '{user_input}':")
            print(f"Sliding Window: {'✓' if sliding_result else '×'} "
                  f"(очікування: {sliding_wait:.1f}с)")
            print(f"Throttling:     {'✓' if throttling_result else '×'} "
                  f"(очікування: {throttling_wait:.1f}с)")
    
    except KeyboardInterrupt:
        print("\n\nДемонстрацію завершено.")


def main():
    """Main function to run both tasks and demonstrations"""
    print("Домашнє завдання 8: Алгоритми контролю потоку та обмеження швидкості")
    print("=" * 80)
    print("Реалізація механізмів обмеження частоти повідомлень у чат-системі")
    print("1. Sliding Window Rate Limiter - точний контроль часових інтервалів")
    print("2. Throttling Rate Limiter - фіксований інтервал між повідомленнями")
    print("=" * 80)
    
    # Track success
    task1_success = False
    task2_success = False
    
    # Run Task 1
    task1_success = run_task1()
    
    # Small delay between tasks
    time.sleep(1)
    
    # Run Task 2
    task2_success = run_task2()
    
    # Compare algorithms
    compare_algorithms()
    
    # Run tests
    print("\n" + "=" * 80)
    tests_success = run_tests()
    
    # Final summary
    print("\n" + "=" * 80)
    print("ПІДСУМОК ВИКОНАННЯ")
    print("=" * 80)
    print(f"Завдання 1 (Sliding Window): {'✅ Виконано' if task1_success else '❌ Помилка'}")
    print(f"Завдання 2 (Throttling):    {'✅ Виконано' if task2_success else '❌ Помилка'}")
    print(f"Тести:                      {'✅ Пройшли' if tests_success else '❌ Помилки'}")
    
    if task1_success and task2_success and tests_success:
        print("\n🎉 Всі завдання успішно виконані!")
        print("\nДоступні можливості:")
        print("- python task1.py (окремо завдання 1)")
        print("- python task2.py (окремо завдання 2)")
        print("- python test_task1.py (тести завдання 1)")
        print("- python test_task2.py (тести завдання 2)")
        
        # Offer interactive demo
        print("\nБажаєте спробувати інтерактивну демонстрацію? (y/n): ", end="")
        try:
            choice = input().lower().strip()
            if choice in ['y', 'yes', 'так', 'т']:
                interactive_demo()
        except (EOFError, KeyboardInterrupt):
            print("\nВихід з програми.")
            
    elif task1_success or task2_success:
        print("\n⚠️ Частково виконано. Перевірте помилки вище.")
    else:
        print("\n💥 Помилки в обох завданнях. Перевірте налаштування.")


if __name__ == "__main__":
    main()
