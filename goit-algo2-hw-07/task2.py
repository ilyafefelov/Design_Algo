"""
Task 2: Performance Comparison of Fibonacci Computation 
using LRU Cache and Splay Tree

This module compares two approaches to caching Fibonacci numbers:
1. LRU Cache with @lru_cache decorator
2. Splay Tree for storing computed values
"""

import time
import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from splay_tree import SplayTree


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    """
    Calculate Fibonacci number using LRU cache decorator
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        n-th Fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    """
    Calculate Fibonacci number using Splay Tree for caching
    
    Args:
        n: Position in Fibonacci sequence
        tree: Splay Tree instance for caching
        
    Returns:
        n-th Fibonacci number
    """
    # Check if value is already in the tree
    cached_value = tree.get(n)
    if cached_value is not None:
        return cached_value
    
    # Base cases
    if n <= 1:
        tree.put(n, n)
        return n
    
    # Recursive calculation
    fib_n = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.put(n, fib_n)
    return fib_n


def measure_time(func, *args, number=10):
    """
    Measure average execution time of a function
    
    Args:
        func: Function to measure
        *args: Arguments to pass to the function
        number: Number of executions for averaging
        
    Returns:
        Average execution time in seconds
    """
    def wrapper():
        return func(*args)
    
    total_time = timeit.timeit(wrapper, number=number)
    return total_time / number


def benchmark_fibonacci():
    """
    Benchmark Fibonacci computation with both approaches
    
    Returns:
        Tuple of (test_values, lru_times, splay_times)
    """
    test_values = list(range(0, 951, 50))  # 0, 50, 100, ..., 950
    lru_times = []
    splay_times = []
    
    print("Benchmark Progress:")
    print("n\t\tLRU Cache Time (s)\tSplay Tree Time (s)")
    print("-" * 60)
    
    for i, n in enumerate(test_values):
        # Clear LRU cache for fair comparison
        fibonacci_lru.cache_clear()
        
        # Create fresh Splay Tree for each test
        tree = SplayTree()
        
        # Measure LRU cache time
        lru_time = measure_time(fibonacci_lru, n, number=3)
        
        # Measure Splay Tree time
        splay_time = measure_time(fibonacci_splay, n, tree, number=3)
        
        lru_times.append(lru_time)
        splay_times.append(splay_time)
        
        print(f"{n}\t\t{lru_time:.8f}\t\t{splay_time:.8f}")
        
        # Progress indicator
        if (i + 1) % 5 == 0:
            progress = (i + 1) / len(test_values) * 100
            print(f"Progress: {progress:.1f}%")
    
    return test_values, lru_times, splay_times


def create_comparison_plot(test_values, lru_times, splay_times):
    """
    Create a comparison plot of execution times
    
    Args:
        test_values: List of n values
        lru_times: List of LRU cache execution times
        splay_times: List of Splay Tree execution times
    """
    plt.figure(figsize=(12, 8))
    
    plt.plot(test_values, lru_times, 'o-', label='LRU Cache', linewidth=2, markersize=6)
    plt.plot(test_values, splay_times, 's-', label='Splay Tree', linewidth=2, markersize=6)
    
    plt.xlabel('Число Фібоначчі (n)', fontsize=12)
    plt.ylabel('Середній час виконання (секунди)', fontsize=12)
    plt.title('Порівняння часу виконання для LRU Cache та Splay Tree', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Format y-axis to show scientific notation
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    plt.tight_layout()
    plt.savefig('fibonacci_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()


def print_results_table(test_values, lru_times, splay_times):
    """
    Print formatted results table
    
    Args:
        test_values: List of n values
        lru_times: List of LRU cache execution times
        splay_times: List of Splay Tree execution times
    """
    print("\n" + "=" * 70)
    print("ДЕТАЛЬНІ РЕЗУЛЬТАТИ БЕНЧМАРКУ")
    print("=" * 70)
    print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
    print("-" * 70)
    
    for n, lru_time, splay_time in zip(test_values, lru_times, splay_times):
        print(f"{n:<10}{lru_time:<25.8f}{splay_time:<25.8f}")
    
    # Calculate statistics
    avg_lru = sum(lru_times) / len(lru_times)
    avg_splay = sum(splay_times) / len(splay_times)
    
    print("-" * 70)
    print(f"{'Середнє:':<10}{avg_lru:<25.8f}{avg_splay:<25.8f}")
    
    # Performance comparison
    if avg_lru < avg_splay:
        ratio = avg_splay / avg_lru
        winner = "LRU Cache"
    else:
        ratio = avg_lru / avg_splay
        winner = "Splay Tree"
    
    print(f"\nВисновок: {winner} в середньому швидший у {ratio:.2f} разів")


def analyze_results(test_values, lru_times, splay_times):
    """
    Analyze and print insights about the results
    
    Args:
        test_values: List of n values
        lru_times: List of LRU cache execution times
        splay_times: List of Splay Tree execution times
    """
    print("\n" + "=" * 70)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("=" * 70)
    
    # Find best and worst cases for each method
    min_lru_idx = lru_times.index(min(lru_times))
    max_lru_idx = lru_times.index(max(lru_times))
    min_splay_idx = splay_times.index(min(splay_times))
    max_splay_idx = splay_times.index(max(splay_times))
    
    print("LRU Cache:")
    print(f"  Найкращий час: {lru_times[min_lru_idx]:.8f}s при n={test_values[min_lru_idx]}")
    print(f"  Найгірший час: {lru_times[max_lru_idx]:.8f}s при n={test_values[max_lru_idx]}")
    
    print("\nSplay Tree:")
    print(f"  Найкращий час: {splay_times[min_splay_idx]:.8f}s при n={test_values[min_splay_idx]}")
    print(f"  Найгірший час: {splay_times[max_splay_idx]:.8f}s при n={test_values[max_splay_idx]}")
    
    # Count wins
    lru_wins = sum(1 for lru, splay in zip(lru_times, splay_times) if lru < splay)
    splay_wins = len(test_values) - lru_wins
    
    print(f"\nПеремоги по тестах:")
    print(f"  LRU Cache: {lru_wins}/{len(test_values)} тестів")
    print(f"  Splay Tree: {splay_wins}/{len(test_values)} тестів")
    
    # Performance insights
    print(f"\nОсновні висновки:")
    
    if lru_wins > splay_wins:
        print("- LRU Cache загалом показує кращу продуктивність")
        print("- Декоратор @lru_cache оптимізований для рекурсивних обчислень")
        print("- Вбудована реалізація має менші накладні витрати")
    else:
        print("- Splay Tree загалом показує кращу продуктивність") 
        print("- Самобалансуюча структура ефективна для частих запитів")
        print("- Адаптивна природа дерева корисна для різних патернів доступу")
    
    print("- Обидва методи значно краще наївної рекурсії")
    print("- Вибір залежить від специфіки застосування та розміру даних")


def main():
    """Main function to run the benchmark and analysis"""
    print("Завдання 2: Порівняння продуктивності обчислення чисел Фібоначчі")
    print("=" * 75)
    print("Порівняння LRU Cache та Splay Tree для кешування")
    print()
    
    # Run benchmark
    print("Запуск бенчмарку...")
    test_values, lru_times, splay_times = benchmark_fibonacci()
    
    # Print detailed results
    print_results_table(test_values, lru_times, splay_times)
    
    # Analyze results
    analyze_results(test_values, lru_times, splay_times)
    
    # Create comparison plot
    print(f"\nСтворення графіка порівняння...")
    create_comparison_plot(test_values, lru_times, splay_times)
    print("Графік збережено як 'fibonacci_comparison.png'")


if __name__ == "__main__":
    main()
