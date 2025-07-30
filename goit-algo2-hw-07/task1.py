"""
Task 1: Data Access Optimization using LRU Cache

This module demonstrates how LRU cache speeds up repeated "hot" queries 
to a large array of numbers.
"""

import random
import time
from lru_cache import LRUCache


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    """
    Generate test queries for array operations
    
    Args:
        n: Array size
        q: Number of queries
        hot_pool: Number of "hot" (frequently used) ranges
        p_hot: Probability of selecting from hot pool for Range queries
        p_update: Probability of Update query
        
    Returns:
        List of queries in format: ("Range", left, right) or ("Update", index, value)
    """
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    
    for _ in range(q):
        if random.random() < p_update:        # ~3% queries are Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% are Range
            if random.random() < p_hot:       # 95% are "hot" ranges
                left, right = random.choice(hot)
            else:                             # 5% are random ranges
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    
    return queries


def range_sum_no_cache(array, left, right):
    """
    Calculate sum of elements in range [left, right] without caching
    
    Args:
        array: Input array
        left: Left index (inclusive)
        right: Right index (inclusive)
        
    Returns:
        Sum of elements in the range
    """
    return sum(array[left:right+1])


def update_no_cache(array, index, value):
    """
    Update array element without caching
    
    Args:
        array: Input array
        index: Index to update
        value: New value
    """
    array[index] = value


def range_sum_with_cache(array, left, right, cache):
    """
    Calculate sum of elements in range [left, right] with LRU caching
    
    Args:
        array: Input array
        left: Left index (inclusive)
        right: Right index (inclusive)
        cache: LRU cache instance
        
    Returns:
        Sum of elements in the range
    """
    key = (left, right)
    result = cache.get(key)
    
    if result == -1:  # Cache miss
        result = sum(array[left:right+1])
        cache.put(key, result)
    
    return result


def update_with_cache(array, index, value, cache):
    """
    Update array element and invalidate affected cache entries
    
    Args:
        array: Input array
        index: Index to update
        value: New value
        cache: LRU cache instance
    """
    array[index] = value
    
    # Invalidate all ranges that contain the updated index
    keys_to_remove = []
    for key in cache.keys():
        left, right = key
        if left <= index <= right:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        cache.remove(key)


def benchmark_queries(array, queries, use_cache=False, cache_capacity=1000):
    """
    Benchmark query execution with or without cache
    
    Args:
        array: Input array (will be modified)
        queries: List of queries to execute
        use_cache: Whether to use caching
        cache_capacity: Cache capacity if using cache
        
    Returns:
        Execution time in seconds
    """
    # Create a copy of array to avoid side effects
    test_array = array.copy()
    
    if use_cache:
        cache = LRUCache(cache_capacity)
    
    start_time = time.time()
    
    for query in queries:
        if query[0] == "Range":
            _, left, right = query
            if use_cache:
                range_sum_with_cache(test_array, left, right, cache)
            else:
                range_sum_no_cache(test_array, left, right)
        
        elif query[0] == "Update":
            _, index, value = query
            if use_cache:
                update_with_cache(test_array, index, value, cache)
            else:
                update_no_cache(test_array, index, value)
    
    end_time = time.time()
    return end_time - start_time


def main():
    """Main function to run the benchmark"""
    print("Завдання 1: Оптимізація доступу до даних за допомогою LRU-кешу")
    print("=" * 65)
    
    # Parameters
    n = 100_000  # Array size
    q = 50_000   # Number of queries
    cache_capacity = 1000
    
    print(f"Параметри тесту:")
    print(f"- Розмір масиву: {n:,}")
    print(f"- Кількість запитів: {q:,}")
    print(f"- Ємність кешу: {cache_capacity}")
    print()
    
    # Generate test data
    print("Генерація тестових даних...")
    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)
    
    # Count query types
    range_count = sum(1 for q in queries if q[0] == "Range")
    update_count = sum(1 for q in queries if q[0] == "Update")
    
    print(f"Згенеровано запитів:")
    print(f"- Range: {range_count:,} ({range_count/len(queries)*100:.1f}%)")
    print(f"- Update: {update_count:,} ({update_count/len(queries)*100:.1f}%)")
    print()
    
    # Benchmark without cache
    print("Виконання тесту без кешу...")
    time_no_cache = benchmark_queries(array, queries, use_cache=False)
    
    # Benchmark with cache
    print("Виконання тесту з LRU-кешем...")
    time_with_cache = benchmark_queries(array, queries, use_cache=True, cache_capacity=cache_capacity)
    
    # Results
    speedup = time_no_cache / time_with_cache if time_with_cache > 0 else float('inf')
    
    print()
    print("РЕЗУЛЬТАТИ:")
    print("=" * 40)
    print(f"Без кешу :  {time_no_cache:.2f} c")
    print(f"LRU-кеш  :  {time_with_cache:.2f} c  (прискорення ×{speedup:.1f})")
    print()
    
    # Additional statistics
    cache_efficiency = ((time_no_cache - time_with_cache) / time_no_cache * 100) if time_no_cache > 0 else 0
    print(f"Ефективність кешування: {cache_efficiency:.1f}%")
    print(f"Зменшення часу виконання: {time_no_cache - time_with_cache:.2f} c")


if __name__ == "__main__":
    random.seed(42)  # For reproducible results
    main()
