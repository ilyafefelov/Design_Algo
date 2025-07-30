"""
Tests for Task 1: LRU Cache optimization
"""

import unittest
import random
from lru_cache import LRUCache
from task1 import (
    range_sum_no_cache, update_no_cache,
    range_sum_with_cache, update_with_cache,
    make_queries, benchmark_queries
)


class TestLRUCache(unittest.TestCase):
    """Test LRU Cache implementation"""
    
    def setUp(self):
        self.cache = LRUCache(3)
    
    def test_put_and_get(self):
        """Test basic put and get operations"""
        self.cache.put(1, 10)
        self.cache.put(2, 20)
        
        self.assertEqual(self.cache.get(1), 10)
        self.assertEqual(self.cache.get(2), 20)
        self.assertEqual(self.cache.get(3), -1)  # Not found
    
    def test_capacity_limit(self):
        """Test cache capacity limit"""
        self.cache.put(1, 10)
        self.cache.put(2, 20)
        self.cache.put(3, 30)
        self.cache.put(4, 40)  # Should evict key 1
        
        self.assertEqual(self.cache.get(1), -1)  # Evicted
        self.assertEqual(self.cache.get(2), 20)
        self.assertEqual(self.cache.get(3), 30)
        self.assertEqual(self.cache.get(4), 40)
    
    def test_lru_behavior(self):
        """Test LRU eviction behavior"""
        self.cache.put(1, 10)
        self.cache.put(2, 20)
        self.cache.put(3, 30)
        
        # Access key 1 to make it recently used
        self.cache.get(1)
        
        # Add new key, should evict key 2 (least recently used)
        self.cache.put(4, 40)
        
        self.assertEqual(self.cache.get(1), 10)  # Still in cache
        self.assertEqual(self.cache.get(2), -1)  # Evicted
        self.assertEqual(self.cache.get(3), 30)
        self.assertEqual(self.cache.get(4), 40)


class TestTask1Functions(unittest.TestCase):
    """Test Task 1 functions"""
    
    def setUp(self):
        self.array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.cache = LRUCache(10)
    
    def test_range_sum_no_cache(self):
        """Test range sum without cache"""
        result = range_sum_no_cache(self.array, 0, 4)
        expected = sum(self.array[0:5])  # 1+2+3+4+5 = 15
        self.assertEqual(result, expected)
    
    def test_range_sum_with_cache(self):
        """Test range sum with cache"""
        # First call should compute and cache
        result1 = range_sum_with_cache(self.array, 0, 4, self.cache)
        expected = sum(self.array[0:5])
        self.assertEqual(result1, expected)
        
        # Second call should use cache
        result2 = range_sum_with_cache(self.array, 0, 4, self.cache)
        self.assertEqual(result2, expected)
        
        # Verify it was cached
        self.assertEqual(self.cache.get((0, 4)), expected)
    
    def test_update_no_cache(self):
        """Test update without cache"""
        original_value = self.array[5]
        update_no_cache(self.array, 5, 100)
        self.assertEqual(self.array[5], 100)
        self.assertNotEqual(self.array[5], original_value)
    
    def test_update_with_cache(self):
        """Test update with cache invalidation"""
        # Cache some ranges
        range_sum_with_cache(self.array, 0, 5, self.cache)
        range_sum_with_cache(self.array, 3, 7, self.cache)
        range_sum_with_cache(self.array, 8, 9, self.cache)
        
        # Update element at index 5
        update_with_cache(self.array, 5, 100, self.cache)
        
        # Ranges containing index 5 should be invalidated
        self.assertEqual(self.cache.get((0, 5)), -1)  # Should be invalidated
        self.assertEqual(self.cache.get((3, 7)), -1)  # Should be invalidated
        self.assertNotEqual(self.cache.get((8, 9)), -1)  # Should remain
    
    def test_make_queries(self):
        """Test query generation"""
        queries = make_queries(100, 1000, hot_pool=10, p_hot=0.9, p_update=0.1)
        
        self.assertEqual(len(queries), 1000)
        
        # Count query types
        range_count = sum(1 for q in queries if q[0] == "Range")
        update_count = sum(1 for q in queries if q[0] == "Update")
        
        self.assertEqual(range_count + update_count, 1000)
        
        # Should have roughly 10% updates (with some variance)
        self.assertGreater(update_count, 50)  # At least 5%
        self.assertLess(update_count, 200)    # At most 20%


class TestBenchmark(unittest.TestCase):
    """Test benchmark functionality"""
    
    def test_benchmark_queries(self):
        """Test benchmark execution"""
        array = [random.randint(1, 100) for _ in range(1000)]
        queries = make_queries(1000, 100)
        
        # Test without cache
        time_no_cache = benchmark_queries(array, queries, use_cache=False)
        self.assertGreater(time_no_cache, 0)
        
        # Test with cache
        time_with_cache = benchmark_queries(array, queries, use_cache=True)
        self.assertGreater(time_with_cache, 0)
        
        # Both should complete successfully
        self.assertIsInstance(time_no_cache, float)
        self.assertIsInstance(time_with_cache, float)


if __name__ == "__main__":
    unittest.main()
