import unittest
import math
from solution import (
    sphere_function, 
    hill_climbing, 
    random_local_search, 
    simulated_annealing,
    generate_random_point,
    generate_neighbor,
    distance
)


class TestOptimizationAlgorithms(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.bounds_2d = [(-5, 5), (-5, 5)]
        self.bounds_3d = [(-5, 5), (-5, 5), (-5, 5)]
        self.epsilon = 1e-6
        self.iterations = 1000
    
    def test_sphere_function(self):
        """Test sphere function calculation"""
        # Test known values
        self.assertEqual(sphere_function([0, 0]), 0)
        self.assertEqual(sphere_function([1, 1]), 2)
        self.assertEqual(sphere_function([2, 3]), 13)
        self.assertEqual(sphere_function([1, 2, 3]), 14)
    
    def test_generate_random_point(self):
        """Test random point generation within bounds"""
        point = generate_random_point(self.bounds_2d)
        self.assertEqual(len(point), 2)
        for i, (lower, upper) in enumerate(self.bounds_2d):
            self.assertGreaterEqual(point[i], lower)
            self.assertLessEqual(point[i], upper)
    
    def test_generate_neighbor(self):
        """Test neighbor generation"""
        point = [0, 0]
        neighbor = generate_neighbor(point, self.bounds_2d, step_size=0.1)
        self.assertEqual(len(neighbor), 2)
        # Neighbor should be close to original point
        self.assertLess(distance(point, neighbor), 0.2)  # Max possible distance with step_size=0.1
    
    def test_distance(self):
        """Test distance calculation"""
        self.assertEqual(distance([0, 0], [0, 0]), 0)
        self.assertEqual(distance([0, 0], [3, 4]), 5)
        self.assertAlmostEqual(distance([1, 1], [2, 2]), math.sqrt(2))
    
    def test_hill_climbing(self):
        """Test Hill Climbing algorithm"""
        solution, value = hill_climbing(sphere_function, self.bounds_2d, iterations=self.iterations)
        
        # Check that solution is within bounds
        for i, (lower, upper) in enumerate(self.bounds_2d):
            self.assertGreaterEqual(solution[i], lower)
            self.assertLessEqual(solution[i], upper)
        
        # Check that value is non-negative (sphere function minimum is 0)
        self.assertGreaterEqual(value, 0)
        
        # Value should match function calculation
        self.assertAlmostEqual(value, sphere_function(solution))
        
        # For sphere function, should find something close to global minimum
        self.assertLess(value, 1.0)  # Should be reasonably close to 0
    
    def test_random_local_search(self):
        """Test Random Local Search algorithm"""
        solution, value = random_local_search(sphere_function, self.bounds_2d, iterations=self.iterations)
        
        # Check that solution is within bounds
        for i, (lower, upper) in enumerate(self.bounds_2d):
            self.assertGreaterEqual(solution[i], lower)
            self.assertLessEqual(solution[i], upper)
        
        # Check that value is non-negative
        self.assertGreaterEqual(value, 0)
        
        # Value should match function calculation
        self.assertAlmostEqual(value, sphere_function(solution))
        
        # For sphere function, should find something close to global minimum
        self.assertLess(value, 2.0)  # Should be reasonably close to 0
    
    def test_simulated_annealing(self):
        """Test Simulated Annealing algorithm"""
        solution, value = simulated_annealing(
            sphere_function, 
            self.bounds_2d, 
            iterations=self.iterations,
            temp=1000,
            cooling_rate=0.95
        )
        
        # Check that solution is within bounds
        for i, (lower, upper) in enumerate(self.bounds_2d):
            self.assertGreaterEqual(solution[i], lower)
            self.assertLessEqual(solution[i], upper)
        
        # Check that value is non-negative
        self.assertGreaterEqual(value, 0)
        
        # Value should match function calculation
        self.assertAlmostEqual(value, sphere_function(solution))
        
        # For sphere function, should find something close to global minimum
        self.assertLess(value, 2.0)  # Should be reasonably close to 0
    
    def test_algorithms_with_3d(self):
        """Test all algorithms with 3D sphere function"""
        algorithms = [
            ("Hill Climbing", hill_climbing),
            ("Random Local Search", random_local_search),
            ("Simulated Annealing", lambda f, b, **kwargs: simulated_annealing(f, b, temp=1000, cooling_rate=0.95, **kwargs))
        ]
        
        for name, algorithm in algorithms:
            with self.subTest(algorithm=name):
                solution, value = algorithm(sphere_function, self.bounds_3d, iterations=500)
                
                # Check dimensions
                self.assertEqual(len(solution), 3)
                
                # Check bounds
                for i, (lower, upper) in enumerate(self.bounds_3d):
                    self.assertGreaterEqual(solution[i], lower)
                    self.assertLessEqual(solution[i], upper)
                
                # Check value
                self.assertGreaterEqual(value, 0)
                self.assertAlmostEqual(value, sphere_function(solution))
    
    def test_convergence_behavior(self):
        """Test that algorithms can achieve good convergence"""
        # Run multiple times and check that at least some runs achieve good results
        good_results = 0
        num_runs = 5
        
        for _ in range(num_runs):
            _, hc_value = hill_climbing(sphere_function, self.bounds_2d, iterations=2000, epsilon=1e-8)
            if hc_value < 0.01:  # Very close to global minimum
                good_results += 1
        
        # At least some runs should achieve good results
        self.assertGreater(good_results, 0)
    
    def test_algorithm_parameters(self):
        """Test algorithms with different parameters"""
        # Test with fewer iterations
        solution, value = hill_climbing(sphere_function, self.bounds_2d, iterations=10)
        self.assertGreaterEqual(value, 0)
        
        # Test with different epsilon
        solution, value = random_local_search(sphere_function, self.bounds_2d, epsilon=1e-3)
        self.assertGreaterEqual(value, 0)
        
        # Test simulated annealing with different temperature settings
        solution, value = simulated_annealing(
            sphere_function, 
            self.bounds_2d, 
            temp=100, 
            cooling_rate=0.99
        )
        self.assertGreaterEqual(value, 0)


class TestEdgeCases(unittest.TestCase):
    
    def test_single_dimension(self):
        """Test with single dimension"""
        bounds = [(-5, 5)]
        solution, value = hill_climbing(sphere_function, bounds, iterations=100)
        self.assertEqual(len(solution), 1)
        self.assertGreaterEqual(solution[0], -5)
        self.assertLessEqual(solution[0], 5)
    
    def test_small_bounds(self):
        """Test with small bounds"""
        bounds = [(-0.1, 0.1), (-0.1, 0.1)]
        solution, value = hill_climbing(sphere_function, bounds, iterations=100)
        # Should find something very close to global minimum
        self.assertLess(value, 0.02)  # 0.1^2 + 0.1^2 = 0.02
    
    def test_zero_iterations(self):
        """Test with zero iterations"""
        bounds = [(-5, 5), (-5, 5)]
        solution, value = hill_climbing(sphere_function, bounds, iterations=0)
        # Should return initial random point
        self.assertEqual(len(solution), 2)
        self.assertGreaterEqual(value, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
