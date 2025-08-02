import random
import time
import matplotlib.pyplot as plt
import copy


def randomized_quick_sort(arr):
    """
    Рандомізований QuickSort - опорний елемент обирається випадково
    """
    if len(arr) <= 1:
        return arr
    
    # Випадковий вибір опорного елемента
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]
    
    # Розділення масиву на три частини
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Рекурсивне сортування лівої та правої частин
    return randomized_quick_sort(left) + middle + randomized_quick_sort(right)


def deterministic_quick_sort(arr):
    """
    Детермінований QuickSort - опорний елемент обирається за фіксованим правилом (середній)
    """
    if len(arr) <= 1:
        return arr
    
    # Вибір середнього елемента як опорного
    pivot_index = len(arr) // 2
    pivot = arr[pivot_index]
    
    # Розділення масиву на три частини
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Рекурсивне сортування лівої та правої частин
    return deterministic_quick_sort(left) + middle + deterministic_quick_sort(right)


def generate_test_array(size):
    """Генерує масив випадкових цілих чисел заданого розміру"""
    return [random.randint(1, 10000) for _ in range(size)]


def measure_sorting_time(sort_function, arr):
    """Вимірює час виконання функції сортування"""
    arr_copy = copy.deepcopy(arr)
    start_time = time.time()
    sort_function(arr_copy)
    end_time = time.time()
    return end_time - start_time


def run_performance_test():
    """Проводить тестування продуктивності обох алгоритмів"""
    # Розміри масивів для тестування
    sizes = [10_000, 50_000, 100_000, 500_000]
    
    # Кількість повторів для більш точної оцінки
    num_runs = 5
    
    results = {
        'sizes': sizes,
        'randomized_times': [],
        'deterministic_times': []
    }
    
    print("Тестування продуктивності QuickSort алгоритмів")
    print("=" * 60)
    
    for size in sizes:
        print(f"Розмір масиву: {size}")
        
        randomized_total_time = 0
        deterministic_total_time = 0
        
        # Проведення кількох тестів для кожного розміру
        for run in range(num_runs):
            # Генерація тестового масиву
            test_array = generate_test_array(size)
            
            # Тестування рандомізованого QuickSort
            randomized_time = measure_sorting_time(randomized_quick_sort, test_array)
            randomized_total_time += randomized_time
            
            # Тестування детермінованого QuickSort
            deterministic_time = measure_sorting_time(deterministic_quick_sort, test_array)
            deterministic_total_time += deterministic_time
        
        # Обчислення середнього часу
        avg_randomized_time = randomized_total_time / num_runs
        avg_deterministic_time = deterministic_total_time / num_runs
        
        results['randomized_times'].append(avg_randomized_time)
        results['deterministic_times'].append(avg_deterministic_time)
        
        print(f"   Рандомізований QuickSort: {avg_randomized_time:.4f} секунд")
        print(f"   Детермінований QuickSort: {avg_deterministic_time:.4f} секунд")
        print()
    
    return results


def create_comparison_plot(results):
    """Створює графік порівняння продуктивності алгоритмів"""
    plt.figure(figsize=(12, 8))
    
    # Основний графік
    plt.plot(results['sizes'], results['randomized_times'], 
             marker='o', linewidth=2, label='Рандомізований QuickSort', color='blue')
    plt.plot(results['sizes'], results['deterministic_times'], 
             marker='s', linewidth=2, label='Детермінований QuickSort', color='orange')
    
    plt.xlabel('Розмір масиву', fontsize=12)
    plt.ylabel('Середній час виконання (секунди)', fontsize=12)
    plt.title('Порівняння рандомізованого та детермінованого QuickSort', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Форматування осей
    plt.ticklabel_format(style='plain', axis='x')
    
    # Збереження графіку
    plt.tight_layout()
    plt.savefig('quicksort_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


def print_performance_table(results):
    """Виводить таблицю результатів тестування"""
    print("=" * 80)
    print("ТАБЛИЦЯ РЕЗУЛЬТАТІВ ТЕСТУВАННЯ")
    print("=" * 80)
    print(f"{'Розмір масиву':<15} {'Рандомізований (с)':<20} {'Детермінований (с)':<20} {'Різниця (%)':<15}")
    print("-" * 80)
    
    for i, size in enumerate(results['sizes']):
        rand_time = results['randomized_times'][i]
        det_time = results['deterministic_times'][i]
        
        # Обчислення відсоткової різниці
        if det_time > 0:
            diff_percent = ((rand_time - det_time) / det_time) * 100
        else:
            diff_percent = 0
        
        print(f"{size:<15} {rand_time:<20.4f} {det_time:<20.4f} {diff_percent:<15.2f}")


def analyze_results(results):
    """Проводить аналіз результатів та робить висновки"""
    print("\n" + "=" * 80)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("=" * 80)
    
    # Середні показники
    avg_randomized = sum(results['randomized_times']) / len(results['randomized_times'])
    avg_deterministic = sum(results['deterministic_times']) / len(results['deterministic_times'])
    
    print(f"Середній час виконання:")
    print(f"  Рандомізований QuickSort: {avg_randomized:.4f} секунд")
    print(f"  Детермінований QuickSort: {avg_deterministic:.4f} секунд")
    
    # Порівняння швидкості
    if avg_randomized < avg_deterministic:
        faster = "рандомізований"
        improvement = ((avg_deterministic - avg_randomized) / avg_deterministic) * 100
    else:
        faster = "детермінований"
        improvement = ((avg_randomized - avg_deterministic) / avg_randomized) * 100
    
    print(f"\nШвидший алгоритм: {faster} (на {improvement:.2f}%)")
    
    # Аналіз стабільності
    rand_variance = sum((t - avg_randomized) ** 2 for t in results['randomized_times']) / len(results['randomized_times'])
    det_variance = sum((t - avg_deterministic) ** 2 for t in results['deterministic_times']) / len(results['deterministic_times'])
    
    print(f"\nСтабільність (дисперсія):")
    print(f"  Рандомізований QuickSort: {rand_variance:.8f}")
    print(f"  Детермінований QuickSort: {det_variance:.8f}")
    
    more_stable = "рандомізований" if rand_variance < det_variance else "детермінований"
    print(f"  Більш стабільний: {more_stable}")
    
    print(f"\nВИСНОВКИ:")
    print("=" * 40)
    print("1. Обидва алгоритми показують схожу продуктивність на випадкових даних")
    print("2. Рандомізований QuickSort менш схильний до найгіршого випадку O(n²)")
    print("3. Детермінований QuickSort більш передбачуваний, але може погано працювати")
    print("   на вже відсортованих або структурованих даних")
    print("4. На практиці рандомізований підхід зазвичай надійніший")


def verify_sorting_correctness():
    """Перевіряє коректність роботи алгоритмів сортування"""
    print("Перевірка коректності сортування...")
    
    # Тестові випадки
    test_cases = [
        [3, 1, 4, 1, 5, 9, 2, 6],
        [1],
        [],
        [5, 5, 5, 5],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        list(range(100))
    ]
    
    for i, test_array in enumerate(test_cases):
        original = test_array.copy()
        
        # Тестування рандомізованого сортування
        sorted_randomized = randomized_quick_sort(test_array.copy())
        
        # Тестування детермінованого сортування
        sorted_deterministic = deterministic_quick_sort(test_array.copy())
        
        # Перевірка коректності
        expected = sorted(original)
        
        if sorted_randomized == expected and sorted_deterministic == expected:
            print(f"  Тест {i+1}: ✓ Пройдено")
        else:
            print(f"  Тест {i+1}: ✗ Помилка")
            print(f"    Оригінал: {original}")
            print(f"    Очікувано: {expected}")
            print(f"    Рандомізований: {sorted_randomized}")
            print(f"    Детермінований: {sorted_deterministic}")
    
    print("Перевірка коректності завершена.\n")


if __name__ == "__main__":
    # Встановлення seed для відтворюваності результатів
    random.seed(42)
    
    print("ЗАВДАННЯ 1: Порівняння рандомізованого та детермінованого QuickSort")
    print("=" * 80)
    
    # Перевірка коректності алгоритмів
    verify_sorting_correctness()
    
    # Проведення тестування продуктивності
    results = run_performance_test()
    
    # Виведення таблиці результатів
    print_performance_table(results)
    
    # Аналіз результатів
    analyze_results(results)
    
    # Створення графіку
    print(f"\nСтворення графіку порівняння...")
    create_comparison_plot(results)
    print("Графік збережено як 'quicksort_comparison.png'")
