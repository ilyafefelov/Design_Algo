import time
import statistics
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
        if len(values) > 1:
            print(f"  Стандартне відхилення: {statistics.stdev(values):.10f}")
        print(f"  Середній час виконання: {statistics.mean(times):.6f} сек")
        
        # Success rate (how often algorithm finds value < 0.01)
        success_count = sum(1 for v in values if v < 0.01)
        success_rate = (success_count / len(values)) * 100
        print(f"  Показник успішності (< 0.01): {success_rate:.1f}%")
        
        # Excellent results rate (how often algorithm finds value < 0.001)
        excellent_count = sum(1 for v in values if v < 0.001)
        excellent_rate = (excellent_count / len(values)) * 100
        print(f"  Відмінні результати (< 0.001): {excellent_rate:.1f}%")
    
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
    
    # Speed ranking
    avg_times = {}
    for algorithm, data in results.items():
        avg_times[algorithm] = statistics.mean(data['times'])
    
    sorted_times = sorted(avg_times.items(), key=lambda x: x[1])
    print(f"\nРейтинг за швидкістю виконання:")
    for i, (algorithm, avg_time) in enumerate(sorted_times, 1):
        print(f"  {i}. {algorithm}: {avg_time:.6f} сек")


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


def detailed_analysis():
    """
    Perform detailed analysis with different parameters
    """
    print("\n" + "=" * 60)
    print("ДЕТАЛЬНИЙ АНАЛІЗ З РІЗНИМИ ПАРАМЕТРАМИ")
    print("=" * 60)
    
    bounds = [(-5, 5), (-5, 5)]
    
    # Test different iteration counts
    print("\n--- Вплив кількості ітерацій ---")
    iteration_counts = [100, 500, 1000, 2000]
    
    for iterations in iteration_counts:
        print(f"\nІтерації: {iterations}")
        hc_solution, hc_value = hill_climbing(sphere_function, bounds, iterations=iterations)
        rls_solution, rls_value = random_local_search(sphere_function, bounds, iterations=iterations)
        sa_solution, sa_value = simulated_annealing(sphere_function, bounds, iterations=iterations)
        
        print(f"  Hill Climbing: {hc_value:.8f}")
        print(f"  Random Local Search: {rls_value:.8f}")
        print(f"  Simulated Annealing: {sa_value:.8f}")
    
    # Test different epsilon values
    print("\n--- Вплив параметра epsilon ---")
    epsilon_values = [1e-3, 1e-4, 1e-5, 1e-6]
    
    for eps in epsilon_values:
        print(f"\nEpsilon: {eps}")
        hc_solution, hc_value = hill_climbing(sphere_function, bounds, epsilon=eps)
        rls_solution, rls_value = random_local_search(sphere_function, bounds, epsilon=eps)
        sa_solution, sa_value = simulated_annealing(sphere_function, bounds, epsilon=eps)
        
        print(f"  Hill Climbing: {hc_value:.8f}")
        print(f"  Random Local Search: {rls_value:.8f}")
        print(f"  Simulated Annealing: {sa_value:.8f}")


if __name__ == "__main__":
    print("БЕНЧМАРК АЛГОРИТМІВ ЛОКАЛЬНОГО ПОШУКУ")
    print("=" * 60)
    
    # Run main benchmark
    results = run_benchmark(num_runs=10, dimensions=2)
    analyze_results(results)
    
    # Compare different dimensions
    compare_dimensions()
    
    # Detailed analysis
    detailed_analysis()
    
    print(f"\n{'ВИСНОВКИ'}")
    print("-" * 30)
    print("1. Hill Climbing зазвичай знаходить найкращі локальні мінімуми")
    print("2. Simulated Annealing більш стабільний завдяки можливості 'втечі' з локальних мінімумів")
    print("3. Random Local Search може бути менш ефективним, але простіший у реалізації")
    print("4. Усі алгоритми показують хорошу збіжність до глобального мінімуму функції Сфери")
    print("5. Збільшення кількості ітерацій покращує результати всіх алгоритмів")
    print("6. Менші значення epsilon дозволяють досягти вищої точності")
