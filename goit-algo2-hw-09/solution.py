import random
import math


# Визначення функції Сфери
def sphere_function(x):
    """
    Sphere function: f(x) = sum(xi^2 for all xi)
    Global minimum is at (0, 0, ..., 0) with value 0
    """
    return sum(xi ** 2 for xi in x)


def generate_random_point(bounds):
    """Generate a random point within the given bounds"""
    return [random.uniform(bound[0], bound[1]) for bound in bounds]


def generate_neighbor(point, bounds, step_size=0.1):
    """Generate a neighbor point by adding small random perturbations"""
    neighbor = []
    for i, (lower, upper) in enumerate(bounds):
        # Add small random perturbation
        perturbation = random.uniform(-step_size, step_size)
        new_value = point[i] + perturbation
        # Ensure the new value is within bounds
        new_value = max(lower, min(upper, new_value))
        neighbor.append(new_value)
    return neighbor


def distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(point1, point2)))


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Hill Climbing algorithm for function minimization.
    
    Args:
        func: Function to minimize
        bounds: List of (min, max) tuples for each dimension
        iterations: Maximum number of iterations
        epsilon: Convergence threshold
    
    Returns:
        tuple: (best_point, best_value)
    """
    # Start with a random point
    current_point = generate_random_point(bounds)
    current_value = func(current_point)
    
    for iteration in range(iterations):
        # Generate a neighbor
        neighbor = generate_neighbor(current_point, bounds)
        neighbor_value = func(neighbor)
        
        # If neighbor is better, move to it
        if neighbor_value < current_value:
            # Check for convergence
            if abs(current_value - neighbor_value) < epsilon or distance(current_point, neighbor) < epsilon:
                current_point = neighbor
                current_value = neighbor_value
                break
            current_point = neighbor
            current_value = neighbor_value
    
    return current_point, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    """
    Random Local Search algorithm for function minimization.
    
    Args:
        func: Function to minimize
        bounds: List of (min, max) tuples for each dimension
        iterations: Maximum number of iterations
        epsilon: Convergence threshold
    
    Returns:
        tuple: (best_point, best_value)
    """
    # Start with a random point
    best_point = generate_random_point(bounds)
    best_value = func(best_point)
    
    for iteration in range(iterations):
        # Generate a random neighbor
        neighbor = generate_neighbor(best_point, bounds)
        neighbor_value = func(neighbor)
        
        # If neighbor is better, update best
        if neighbor_value < best_value:
            # Check for convergence
            if abs(best_value - neighbor_value) < epsilon or distance(best_point, neighbor) < epsilon:
                best_point = neighbor
                best_value = neighbor_value
                break
            best_point = neighbor
            best_value = neighbor_value
    
    return best_point, best_value


# Simulated Annealing
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    """
    Simulated Annealing algorithm for function minimization.
    
    Args:
        func: Function to minimize
        bounds: List of (min, max) tuples for each dimension
        iterations: Maximum number of iterations
        temp: Initial temperature
        cooling_rate: Temperature cooling rate (0 < cooling_rate < 1)
        epsilon: Convergence threshold
    
    Returns:
        tuple: (best_point, best_value)
    """
    # Start with a random point
    current_point = generate_random_point(bounds)
    current_value = func(current_point)
    
    best_point = current_point[:]
    best_value = current_value
    
    current_temp = temp
    
    for iteration in range(iterations):
        # Check temperature convergence
        if current_temp < epsilon:
            break
            
        # Generate a neighbor
        neighbor = generate_neighbor(current_point, bounds)
        neighbor_value = func(neighbor)
        
        # Calculate the difference
        delta = neighbor_value - current_value
        
        # Accept or reject the neighbor
        if delta < 0:  # Better solution
            # Check for convergence
            if abs(delta) < epsilon or distance(current_point, neighbor) < epsilon:
                current_point = neighbor
                current_value = neighbor_value
                if neighbor_value < best_value:
                    best_point = neighbor[:]
                    best_value = neighbor_value
                break
            current_point = neighbor
            current_value = neighbor_value
            # Update best if necessary
            if neighbor_value < best_value:
                best_point = neighbor[:]
                best_value = neighbor_value
        else:  # Worse solution - accept with probability
            probability = math.exp(-delta / current_temp)
            if random.random() < probability:
                current_point = neighbor
                current_value = neighbor_value
        
        # Cool down the temperature
        current_temp *= cooling_rate
    
    return best_point, best_value


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]
    
    print("Мінімізація функції Сфери f(x) = x1² + x2²")
    print("Межі: x1, x2 ∈ [-5, 5]")
    print("Глобальний мінімум: (0, 0) з значенням 0")
    print("=" * 50)
    
    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print(f"Розв'язок: {hc_solution}")
    print(f"Значення: {hc_value}")
    
    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print(f"Розв'язок: {rls_solution}")
    print(f"Значення: {rls_value}")
    
    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print(f"Розв'язок: {sa_solution}")
    print(f"Значення: {sa_value}")
    
    print("\n" + "=" * 50)
    print("Порівняння результатів:")
    results = [
        ("Hill Climbing", hc_value),
        ("Random Local Search", rls_value),
        ("Simulated Annealing", sa_value)
    ]
    results.sort(key=lambda x: x[1])
    
    for i, (method, value) in enumerate(results, 1):
        print(f"{i}. {method}: {value:.10f}")
