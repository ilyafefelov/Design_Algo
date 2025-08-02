import time
import statistics
import matplotlib.pyplot as plt
from solution import sphere_function, hill_climbing, random_local_search, simulated_annealing


def run_benchmark(num_runs=10, dimensions=2):
    """
    Benchmark all three algorithms multiple times and collect statistics
    """
    # Define bounds for the given dimensions
    bounds = [(-5, 5)] * dimensions
    
    results = {
        'Hill Climbing': {'values': [], 'times': [], 'solutions': []},
        'Random Local Search': {'values': [], 'times': [], 'solutions': []},
        'Simulated Annealing': {'values': [], 'times': [], 'solutions': []}
    }
    
    print(f"Запуск бенчмарку для {dimensions}D функції Сфери ({num_runs} прогонів)...")
    print("=" * 60)
    
    for run in range(num_runs):
        print(f"Прогін {run + 1}/{num_runs}")
        
        # Hill Climbing
        start_time = time.time()
        hc_solution, hc_value = hill_climbing(sphere_function, bounds, iterations=1000)
        hc_time = time.time() - start_time
        results['Hill Climbing']['values'].append(hc_value)
        results['Hill Climbing']['times'].append(hc_time)
        results['Hill Climbing']['solutions'].append(hc_solution)
        
        # Random Local Search
        start_time = time.time()
        rls_solution, rls_value = random_local_search(sphere_function, bounds, iterations=1000)
        rls_time = time.time() - start_time
        results['Random Local Search']['values'].append(rls_value)
        results['Random Local Search']['times'].append(rls_time)
        results['Random Local Search']['solutions'].append(rls_solution)
        
        # Simulated Annealing
        start_time = time.time()
        sa_solution, sa_value = simulated_annealing(sphere_function, bounds, iterations=1000)
        sa_time = time.time() - start_time
        results['Simulated Annealing']['values'].append(sa_value)
        results['Simulated Annealing']['times'].append(sa_time)
        results['Simulated Annealing']['solutions'].append(sa_solution)
    
    return results


def analyze_results(results):
    """
    Analyze and display benchmark results
    """
    print("\n" + "=" * 60)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("=" * 60)
    
    # Statistics for each algorithm
    for algorithm, data in results.items():
        values = data['values']
        times = data['times']
        
        print(f"\n{algorithm}:")
        print(f"  Найкраще значення: {min(values):.10f}")
        print(f"  Найгірше значення: {max(values):.10f}")
        print(f"  Середнє значення: {statistics.mean(values):.10f}")
        print(f"  Медіана: {statistics.median(values):.10f}")
        print(f"  Стандартне відхилення: {statistics.stdev(values):.10f}")
        print(f"  Середній час виконання: {statistics.mean(times):.6f} сек")
        
        # Success rate (how often algorithm finds value < 0.01)
        success_count = sum(1 for v in values if v < 0.01)
        success_rate = (success_count / len(values)) * 100
        print(f"  Показник успішності (< 0.01): {success_rate:.1f}%")
    
    # Best overall performance
    print(f"\n{'ПІДСУМКИ'}")
    print("-" * 30)
    
    best_values = {}
    for algorithm, data in results.items():
        best_values[algorithm] = min(data['values'])
    
    best_algorithm = min(best_values, key=best_values.get)
    print(f"Найкращий результат: {best_algorithm} ({best_values[best_algorithm]:.10f})")
    
    # Average performance ranking
    avg_values = {}
    for algorithm, data in results.items():
        avg_values[algorithm] = statistics.mean(data['values'])
    
    sorted_avg = sorted(avg_values.items(), key=lambda x: x[1])
    print(f"\nРейтинг за середнім результатом:")
    for i, (algorithm, avg_value) in enumerate(sorted_avg, 1):
        print(f"  {i}. {algorithm}: {avg_value:.10f}")


def plot_results(results, save_path=None):
    """
    Create visualizations of the benchmark results
    """
    try:
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Порівняння алгоритмів оптимізації функції Сфери', fontsize=16)
        
        algorithms = list(results.keys())
        colors = ['blue', 'green', 'red']
        
        # 1. Box plot of function values
        values_data = [results[alg]['values'] for alg in algorithms]
        ax1.boxplot(values_data, tick_labels=algorithms)
        ax1.set_title('Розподіл значень функції')
        ax1.set_ylabel('Значення функції')
        ax1.set_yscale('log')
        
        # 2. Execution times
        times_data = [results[alg]['times'] for alg in algorithms]
        ax2.boxplot(times_data, tick_labels=algorithms)
        ax2.set_title('Час виконання')
        ax2.set_ylabel('Час (сек)')
        
        # 3. Best values comparison
        best_values = [min(results[alg]['values']) for alg in algorithms]
        bars = ax3.bar(algorithms, best_values, color=colors)
        ax3.set_title('Найкращі знайдені значення')
        ax3.set_ylabel('Значення функції')
        ax3.set_yscale('log')
        
        # Add value labels on bars
        for bar, value in zip(bars, best_values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2e}', ha='center', va='bottom')
        
        # 4. Success rate (percentage of runs with value < 0.01)
        success_rates = []
        for alg in algorithms:
            success_count = sum(1 for v in results[alg]['values'] if v < 0.01)
            success_rate = (success_count / len(results[alg]['values'])) * 100
            success_rates.append(success_rate)
        
        bars = ax4.bar(algorithms, success_rates, color=colors)
        ax4.set_title('Показник успішності (значення < 0.01)')
        ax4.set_ylabel('Відсоток успішних прогонів (%)')
        ax4.set_ylim(0, 100)
        
        # Add percentage labels on bars
        for bar, rate in zip(bars, success_rates):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{rate:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nГрафік збережено як: {save_path}")
        
        plt.show()
        
    except ImportError:
        print("\nMatplotlib не встановлено. Пропуск візуалізації.")
        print("Для встановлення: pip install matplotlib")


def compare_dimensions():
    """
    Compare algorithm performance across different dimensions
    """
    print("\n" + "=" * 60)
    print("ПОРІВНЯННЯ ПО РОЗМІРНОСТЯХ")
    print("=" * 60)
    
    dimensions = [2, 3, 5]
    
    for dim in dimensions:
        print(f"\n--- {dim}D Функція Сфери ---")
        bounds = [(-5, 5)] * dim
        
        # Single run for each algorithm
        hc_solution, hc_value = hill_climbing(sphere_function, bounds, iterations=1000)
        rls_solution, rls_value = random_local_search(sphere_function, bounds, iterations=1000)
        sa_solution, sa_value = simulated_annealing(sphere_function, bounds, iterations=1000)
        
        print(f"Hill Climbing: {hc_value:.8f}")
        print(f"Random Local Search: {rls_value:.8f}")
        print(f"Simulated Annealing: {sa_value:.8f}")


if __name__ == "__main__":
    print("БЕНЧМАРК АЛГОРИТМІВ ЛОКАЛЬНОГО ПОШУКУ")
    print("=" * 60)
    
    # Run main benchmark
    results = run_benchmark(num_runs=10, dimensions=2)
    analyze_results(results)
    
    # Create visualization
    plot_results(results, save_path="optimization_benchmark.png")
    
    # Compare different dimensions
    compare_dimensions()
    
    print(f"\n{'ВИСНОВКИ'}")
    print("-" * 30)
    print("1. Hill Climbing зазвичай знаходить найкращі локальні мінімуми")
    print("2. Simulated Annealing більш стабільний завдяки можливості 'втечі' з локальних мінімумів")
    print("3. Random Local Search може бути менш ефективним, але простіший у реалізації")
    print("4. Усі алгоритми показують хорошу збіжність до глобального мінімуму функції Сфери")
