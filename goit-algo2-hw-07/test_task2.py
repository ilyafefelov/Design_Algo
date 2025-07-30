"""
Tests for Task 2: Fibonacci computation comparison
"""

import unittest
from unittest.mock import patch
from splay_tree import SplayTree, SplayTreeNode
from task2 import fibonacci_lru, fibonacci_splay, measure_time


class TestSplayTree(unittest.TestCase):
    """Test Splay Tree implementation"""
    
    def setUp(self):
        self.tree = SplayTree()
    
    def test_insert_and_search(self):
        """Test basic insert and search operations"""
        self.tree.insert(5, 'five')
        self.tree.insert(3, 'three')
        self.tree.insert(7, 'seven')
        
        self.assertEqual(self.tree.search(5), 'five')
        self.assertEqual(self.tree.search(3), 'three')
        self.assertEqual(self.tree.search(7), 'seven')
        self.assertIsNone(self.tree.search(10))
    
    def test_splay_operation(self):
        """Test that search moves element to root"""
        self.tree.insert(5, 'five')
        self.tree.insert(3, 'three')
        self.tree.insert(7, 'seven')
        
        # Search for 3 should move it to root
        self.tree.search(3)
        self.assertEqual(self.tree.root.key, 3)
        self.assertEqual(self.tree.root.value, 'three')
    
    def test_update_existing_key(self):
        """Test updating existing key"""
        self.tree.insert(5, 'five')
        self.tree.insert(5, 'FIVE')  # Update
        
        self.assertEqual(self.tree.search(5), 'FIVE')


class TestFibonacciLRU(unittest.TestCase):
    """Test Fibonacci with LRU cache"""
    
    def setUp(self):
        # Clear cache before each test
        fibonacci_lru.cache_clear()
    
    def test_base_cases(self):
        """Test Fibonacci base cases"""
        self.assertEqual(fibonacci_lru(0), 0)
        self.assertEqual(fibonacci_lru(1), 1)
    
    def test_small_numbers(self):
        """Test Fibonacci for small numbers"""
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, exp in enumerate(expected):
            self.assertEqual(fibonacci_lru(i), exp)
    
    def test_cache_info(self):
        """Test that caching is working"""
        fibonacci_lru.cache_clear()
        
        # Calculate fibonacci(10)
        result = fibonacci_lru(10)
        cache_info = fibonacci_lru.cache_info()
        
        # Should have some cache hits from recursive calls
        self.assertGreater(cache_info.hits, 0)
        self.assertEqual(result, 55)  # 10th Fibonacci number


class TestFibonacciSplay(unittest.TestCase):
    """Test Fibonacci with Splay Tree"""
    
    def setUp(self):
        self.tree = SplayTree()
    
    def test_base_cases(self):
        """Test Fibonacci base cases"""
        self.assertEqual(fibonacci_splay(0, self.tree), 0)
        self.assertEqual(fibonacci_splay(1, self.tree), 1)
    
    def test_small_numbers(self):
        """Test Fibonacci for small numbers"""
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, exp in enumerate(expected):
            tree = SplayTree()  # Fresh tree for each test
            result = fibonacci_splay(i, tree)
            self.assertEqual(result, exp)
    
    def test_caching_behavior(self):
        """Test that results are cached in tree"""
        result = fibonacci_splay(5, self.tree)
        
        # Check that intermediate results are cached
        self.assertEqual(self.tree.search(0), 0)
        self.assertEqual(self.tree.search(1), 1)
        self.assertEqual(self.tree.search(2), 1)
        self.assertEqual(self.tree.search(3), 2)
        self.assertEqual(self.tree.search(4), 3)
        self.assertEqual(self.tree.search(5), 5)
        
        self.assertEqual(result, 5)
    
    def test_reuse_cached_values(self):
        """Test that cached values are reused"""
        # Calculate fibonacci(5) - this will cache 0-5
        fibonacci_splay(5, self.tree)
        
        # Now calculate fibonacci(6) - should reuse cached values
        result = fibonacci_splay(6, self.tree)
        
        # Result should be correct
        self.assertEqual(result, 8)
        
        # And fibonacci(6) should now be cached
        self.assertEqual(self.tree.search(6), 8)


class TestMeasureTime(unittest.TestCase):
    """Test time measurement utility"""
    
    def test_measure_time_basic(self):
        """Test basic time measurement"""
        def dummy_function():
            return sum(range(1000))
        
        time_taken = measure_time(dummy_function, number=5)
        
        # Should return a positive float
        self.assertIsInstance(time_taken, float)
        self.assertGreater(time_taken, 0)
    
    def test_measure_time_with_args(self):
        """Test time measurement with function arguments"""
        def add_numbers(a, b):
            return a + b
        
        time_taken = measure_time(add_numbers, 5, 10, number=3)
        
        # Should return a positive float
        self.assertIsInstance(time_taken, float)
        self.assertGreater(time_taken, 0)


class TestFibonacciComparison(unittest.TestCase):
    """Test comparison between methods"""
    
    def test_same_results(self):
        """Test that both methods produce same results"""
        fibonacci_lru.cache_clear()
        tree = SplayTree()
        
        test_values = [0, 1, 5, 10, 15, 20]
        
        for n in test_values:
            lru_result = fibonacci_lru(n)
            splay_result = fibonacci_splay(n, tree)
            
            self.assertEqual(lru_result, splay_result,
                           f"Results differ for n={n}: LRU={lru_result}, Splay={splay_result}")


if __name__ == "__main__":
    unittest.main()
