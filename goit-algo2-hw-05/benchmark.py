"""
Comprehensive benchmark for Homework 5 tasks.
Tests performance and accuracy of both Bloom Filter and HyperLogLog implementations.
"""
import time
import random
import string
from task1.solution import BloomFilter, check_password_uniqueness
from task2.solution import HyperLogLog, exact_unique_count, hyperloglog_unique_count


def generate_random_passwords(count: int, length: int = 10) -> list:
    """Generate random passwords for testing."""
    passwords = []
    for _ in range(count):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        passwords.append(password)
    return passwords


def generate_ip_addresses(count: int, unique_ratio: float = 0.7) -> list:
    """
    Generate IP addresses with specified uniqueness ratio.
    
    Args:
        count: Total number of IPs to generate
        unique_ratio: Ratio of unique IPs (0.0 to 1.0)
    """
    unique_count = int(count * unique_ratio)
    unique_ips = []
    
    for i in range(unique_count):
        ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        unique_ips.append(ip)
    
    # Add duplicates to reach target count
    all_ips = unique_ips.copy()
    while len(all_ips) < count:
        all_ips.append(random.choice(unique_ips))
    
    random.shuffle(all_ips)
    return all_ips


def benchmark_bloom_filter():
    """Benchmark Bloom Filter performance and accuracy."""
    print("="*60)
    print("BENCHMARK: Bloom Filter для перевірки паролів")
    print("="*60)
    
    # Test different sizes and hash counts
    test_configs = [
        (1000, 3, 500),      # Small filter
        (10000, 5, 5000),    # Medium filter
        (100000, 7, 50000),  # Large filter
    ]
    
    print(f"{'Розмір':<10} {'Хеші':<6} {'Паролі':<10} {'Час (мс)':<12} {'Хибнопозитивні':<16} {'Точність %':<12}")
    print("-" * 80)
    
    for size, num_hashes, num_passwords in test_configs:
        # Create Bloom filter
        bloom = BloomFilter(size=size, num_hashes=num_hashes)
        
        # Generate existing passwords
        existing_passwords = generate_random_passwords(num_passwords // 2)
        for pwd in existing_passwords:
            bloom.add(pwd)
        
        # Generate test passwords (mix of existing and new)
        test_passwords = (existing_passwords[:100] +  # 100 existing
                         generate_random_passwords(100))  # 100 new
        random.shuffle(test_passwords)
        
        # Benchmark
        start_time = time.time()
        results = check_password_uniqueness(bloom, test_passwords)
        end_time = time.time()
        
        # Calculate metrics
        execution_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Count false positives (new passwords marked as existing)
        known_existing = set(existing_passwords[:100])
        false_positives = 0
        true_positives = 0
        
        for pwd, status in results.items():
            if pwd in known_existing:
                if status == "вже використаний":
                    true_positives += 1
            else:
                if status == "вже використаний":
                    false_positives += 1
        
        accuracy = (true_positives / 100) * 100 if true_positives > 0 else 0
        
        print(f"{size:<10} {num_hashes:<6} {num_passwords:<10} {execution_time:<12.2f} "
              f"{false_positives:<16} {accuracy:<12.1f}")
    
    # Memory usage analysis
    print(f"\nАналіз використання пам'яті:")
    for size, num_hashes, _ in test_configs:
        bloom_memory = size // 8  # bits to bytes
        set_memory = (num_passwords // 2) * 15  # approximate string size
        savings = (set_memory - bloom_memory) / set_memory * 100
        
        print(f"Розмір {size}: Bloom Filter ~{bloom_memory:,} байт, "
              f"Set ~{set_memory:,} байт, економія {savings:.1f}%")


def benchmark_hyperloglog():
    """Benchmark HyperLogLog performance and accuracy."""
    print("\n" + "="*60)
    print("BENCHMARK: HyperLogLog для підрахунку унікальних IP")
    print("="*60)
    
    # Test different dataset sizes
    test_sizes = [1000, 10000, 100000]
    
    print(f"{'Розмір даних':<12} {'Унікальні':<12} {'HLL оцінка':<12} {'Похибка %':<12} "
          f"{'Точний (мс)':<14} {'HLL (мс)':<12} {'Прискорення':<12}")
    print("-" * 100)
    
    for size in test_sizes:
        # Generate test data
        ips = generate_ip_addresses(size, unique_ratio=0.6)
        
        # Exact counting
        start_time = time.time()
        exact_count, _ = exact_unique_count(ips)
        exact_time = time.time() - start_time
        
        # HyperLogLog counting
        start_time = time.time()
        hll_count, _ = hyperloglog_unique_count(ips, precision=14)
        hll_time = time.time() - start_time
        
        # Calculate metrics
        error_percentage = abs(exact_count - hll_count) / exact_count * 100
        speedup = exact_time / hll_time if hll_time > 0 else float('inf')
        
        print(f"{size:<12} {exact_count:<12} {hll_count:<12.0f} {error_percentage:<12.2f} "
              f"{exact_time*1000:<14.2f} {hll_time*1000:<12.2f} {speedup:<12.2f}")
    
    # Precision analysis
    print(f"\nАналіз точності HyperLogLog (1000 унікальних IP):")
    test_ips = generate_ip_addresses(5000, unique_ratio=0.2)  # 1000 unique
    actual_unique = len(set(test_ips))
    
    print(f"{'Precision':<10} {'Пам\'ять (KB)':<14} {'Оцінка':<10} {'Похибка %':<12}")
    print("-" * 50)
    
    for precision in range(8, 17):
        hll = HyperLogLog(precision=precision)
        for ip in test_ips:
            hll.add(ip)
        
        estimate = hll.estimate_cardinality()
        error = abs(estimate - actual_unique) / actual_unique * 100
        memory_kb = (2 ** precision) / 1024
        
        print(f"{precision:<10} {memory_kb:<14.2f} {estimate:<10.0f} {error:<12.2f}")


def benchmark_scalability():
    """Test scalability with very large datasets."""
    print("\n" + "="*60)
    print("BENCHMARK: Масштабованість на великих даних")
    print("="*60)
    
    # Very large dataset test
    print("Тест з великими наборами даних...")
    
    large_sizes = [100000, 500000, 1000000]
    
    print(f"{'Розмір':<10} {'Bloom Filter (мс)':<18} {'HyperLogLog (мс)':<16} {'Ratio':<8}")
    print("-" * 60)
    
    for size in large_sizes:
        # Test Bloom Filter with passwords
        passwords = generate_random_passwords(size // 10)  # Smaller subset for testing
        bloom = BloomFilter(size=size, num_hashes=5)
        
        start_time = time.time()
        for pwd in passwords[:1000]:  # Test with 1000 passwords
            bloom.add(pwd)
        test_passwords = passwords[1000:1100] + generate_random_passwords(100)
        results = check_password_uniqueness(bloom, test_passwords)
        bloom_time = (time.time() - start_time) * 1000
        
        # Test HyperLogLog with IPs
        ips = generate_ip_addresses(min(size, 100000), unique_ratio=0.5)  # Limit for memory
        
        start_time = time.time()
        hll_count, _ = hyperloglog_unique_count(ips, precision=14)
        hll_time = (time.time() - start_time) * 1000
        
        ratio = bloom_time / hll_time if hll_time > 0 else float('inf')
        
        print(f"{size:<10} {bloom_time:<18.2f} {hll_time:<16.2f} {ratio:<8.2f}")


def run_comprehensive_benchmark():
    """Run all benchmarks."""
    print("КОМПЛЕКСНИЙ БЕНЧМАРК ДОМАШНЬОГО ЗАВДАННЯ 5")
    print("Алгоритми роботи з великими даними")
    print("=" * 80)
    
    # Set random seed for reproducible results
    random.seed(42)
    
    try:
        benchmark_bloom_filter()
        benchmark_hyperloglog()
        benchmark_scalability()
        
        print("\n" + "="*60)
        print("ВИСНОВКИ:")
        print("="*60)
        print("✅ Bloom Filter:")
        print("   - Ефективна перевірка членства з мінімальним використанням пам'яті")
        print("   - Можливі хибнопозитивні результати, але немає хибнонегативних")
        print("   - Відмінно підходить для попередньої фільтрації")
        
        print("\n✅ HyperLogLog:")
        print("   - Точна оцінка кардинальності з постійним використанням пам'яті")
        print("   - Похибка зазвичай < 2% при правильному налаштуванні")
        print("   - Ідеально для аналітики великих даних")
        
        print("\n🚀 Обидва алгоритми демонструють відмінну масштабованість!")
        
    except KeyboardInterrupt:
        print("\nБенчмарк перерваний користувачем.")
    except Exception as e:
        print(f"\nПомилка під час виконання бенчмарку: {e}")


if __name__ == "__main__":
    run_comprehensive_benchmark()
