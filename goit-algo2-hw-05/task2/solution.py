import re
import time
import hashlib
import math
from typing import Set, List, Tuple
import requests
import os


class HyperLogLog:
    """
    HyperLogLog implementation for cardinality estimation.
    
    HyperLogLog is a probabilistic cardinality estimator that can estimate
    the number of distinct elements in a multiset with very low memory usage.
    """
    
    def __init__(self, precision: int = 14):
        """
        Initialize HyperLogLog with given precision.
        
        Args:
            precision (int): Precision parameter (4 <= precision <= 16)
                           Higher precision = more accuracy but more memory
        """
        if not (4 <= precision <= 16):
            raise ValueError("Precision must be between 4 and 16")
        
        self.precision = precision
        self.m = 2 ** precision  # Number of buckets
        self.buckets = [0] * self.m
        
        # Alpha constant for bias correction
        if self.m >= 128:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)
        elif self.m >= 64:
            self.alpha = 0.709
        elif self.m >= 32:
            self.alpha = 0.697
        else:
            self.alpha = 0.5
    
    def _hash(self, item: str) -> int:
        """
        Hash an item using SHA-1.
        
        Args:
            item (str): Item to hash
            
        Returns:
            int: 64-bit hash value
        """
        return int(hashlib.sha1(item.encode('utf-8')).hexdigest(), 16)
    
    def add(self, item: str) -> None:
        """
        Add an item to the HyperLogLog.
        
        Args:
            item (str): Item to add
        """
        if not isinstance(item, str):
            raise TypeError("Item must be a string")
        
        # Get hash value
        hash_value = self._hash(item)
        
        # Use first 'precision' bits for bucket index
        bucket_index = hash_value & ((1 << self.precision) - 1)
        
        # Use remaining bits to count leading zeros
        remaining_bits = hash_value >> self.precision
        leading_zeros = self._count_leading_zeros(remaining_bits) + 1
        
        # Update bucket with maximum leading zeros seen
        self.buckets[bucket_index] = max(self.buckets[bucket_index], leading_zeros)
    
    def _count_leading_zeros(self, value: int) -> int:
        """
        Count leading zeros in a 64-bit integer.
        
        Args:
            value (int): Integer value
            
        Returns:
            int: Number of leading zeros
        """
        if value == 0:
            return 64 - self.precision
        
        count = 0
        # We work with 64-bit values minus precision bits
        bit_length = 64 - self.precision
        
        for i in range(bit_length):
            if value & (1 << (bit_length - 1 - i)):
                break
            count += 1
        
        return count
    
    def estimate_cardinality(self) -> float:
        """
        Estimate the cardinality (number of unique elements).
        
        Returns:
            float: Estimated cardinality
        """
        # Calculate raw estimate
        raw_estimate = self.alpha * (self.m ** 2) / sum(2 ** (-x) for x in self.buckets)
        
        # Apply small range correction
        if raw_estimate <= 2.5 * self.m:
            # Small range correction
            zeros = self.buckets.count(0)
            if zeros != 0:
                return self.m * math.log(self.m / zeros)
        
        # Large range correction
        if raw_estimate <= (1.0/30.0) * (2 ** 32):
            return raw_estimate
        else:
            return -2 ** 32 * math.log(1 - raw_estimate / (2 ** 32))
        
        return raw_estimate


def download_log_file(url: str, filename: str) -> bool:
    """
    Download log file if it doesn't exist.
    
    Args:
        url (str): URL to download from
        filename (str): Local filename to save
        
    Returns:
        bool: True if file exists or was downloaded successfully
    """
    if os.path.exists(filename):
        print(f"Файл {filename} вже існує.")
        return True
    
    try:
        print(f"Завантаження файлу {filename}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Файл {filename} успішно завантажено.")
        return True
    except Exception as e:
        print(f"Помилка завантаження файлу: {e}")
        return False


def extract_ips_from_log(filename: str) -> List[str]:
    """
    Extract IP addresses from log file.
    
    Args:
        filename (str): Path to log file
        
    Returns:
        List[str]: List of IP addresses found in the log
    """
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = []
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    # Find all IP addresses in the line
                    found_ips = ip_pattern.findall(line)
                    ips.extend(found_ips)
                except Exception as e:
                    # Skip problematic lines
                    print(f"Пропускаємо рядок {line_num}: {e}")
                    continue
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
        return []
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return []
    
    return ips


def exact_unique_count(ips: List[str]) -> Tuple[int, float]:
    """
    Count unique IP addresses using exact method (set).
    
    Args:
        ips (List[str]): List of IP addresses
        
    Returns:
        Tuple[int, float]: (unique count, execution time)
    """
    start_time = time.time()
    unique_ips = set(ips)
    end_time = time.time()
    
    return len(unique_ips), end_time - start_time


def hyperloglog_unique_count(ips: List[str], precision: int = 14) -> Tuple[float, float]:
    """
    Count unique IP addresses using HyperLogLog.
    
    Args:
        ips (List[str]): List of IP addresses
        precision (int): HyperLogLog precision parameter
        
    Returns:
        Tuple[float, float]: (estimated count, execution time)
    """
    start_time = time.time()
    
    hll = HyperLogLog(precision=precision)
    for ip in ips:
        hll.add(ip)
    
    estimate = hll.estimate_cardinality()
    end_time = time.time()
    
    return estimate, end_time - start_time


def create_sample_log_file(filename: str, num_lines: int = 10000) -> None:
    """
    Create a sample log file for testing if the real one is not available.
    
    Args:
        filename (str): Filename to create
        num_lines (int): Number of log lines to generate
    """
    import random
    
    print(f"Створення тестового файлу {filename} з {num_lines} рядками...")
    
    with open(filename, 'w') as f:
        for i in range(num_lines):
            # Generate random IP address
            ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            timestamp = f"2024-01-01 12:00:{i%60:02d}"
            log_line = f"{ip} - - [{timestamp}] \"GET /page HTTP/1.1\" 200 1234\n"
            f.write(log_line)
    
    print(f"Тестовий файл {filename} створено.")


def compare_methods(log_filename: str) -> None:
    """
    Compare exact and HyperLogLog methods for counting unique IPs.
    
    Args:
        log_filename (str): Path to log file
    """
    print("Завантаження та обробка лог-файлу...")
    
    # Try to download the real log file first
    log_url = "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/apache_logs/apache_logs"
    
    if not download_log_file(log_url, log_filename):
        # If download fails, create a sample file
        create_sample_log_file(log_filename, 50000)
    
    # Extract IP addresses
    ips = extract_ips_from_log(log_filename)
    
    if not ips:
        print("Не знайдено IP-адрес у файлі.")
        return
    
    print(f"Знайдено {len(ips)} IP-адрес у лог-файлі.")
    
    # Exact count
    print("\nВиконання точного підрахунку...")
    exact_count, exact_time = exact_unique_count(ips)
    
    # HyperLogLog count
    print("Виконання HyperLogLog підрахунку...")
    hll_count, hll_time = hyperloglog_unique_count(ips)
    
    # Calculate error
    error_percentage = abs(exact_count - hll_count) / exact_count * 100
    
    # Display results
    print("\n" + "="*60)
    print("Результати порівняння:")
    print("="*60)
    print(f"{'Метод':<25} {'Унікальні елементи':<20} {'Час виконання (сек.)':<20}")
    print("-" * 60)
    print(f"{'Точний підрахунок':<25} {exact_count:<20.0f} {exact_time:<20.4f}")
    print(f"{'HyperLogLog':<25} {hll_count:<20.0f} {hll_time:<20.4f}")
    print("-" * 60)
    print(f"Похибка HyperLogLog: {error_percentage:.2f}%")
    print(f"Прискорення: {exact_time/hll_time:.2f}x")
    
    # Memory usage estimation
    exact_memory = len(set(ips)) * 15  # Approximate bytes per IP string
    hll_memory = 2 ** 14 * 1  # HyperLogLog buckets
    memory_savings = (exact_memory - hll_memory) / exact_memory * 100
    
    print(f"\nОцінка використання пам'яті:")
    print(f"Точний метод: ~{exact_memory:,} байт")
    print(f"HyperLogLog: ~{hll_memory:,} байт")
    print(f"Економія пам'яті: {memory_savings:.1f}%")


if __name__ == "__main__":
    # Test with different file names
    log_files = ["lms-stage-access.log", "sample-access.log"]
    
    for log_file in log_files:
        if os.path.exists(log_file) or log_file == "sample-access.log":
            print(f"\n{'='*80}")
            print(f"Аналіз файлу: {log_file}")
            print(f"{'='*80}")
            compare_methods(log_file)
            break
    else:
        # If no files exist, create and test with sample
        print("Створення тестового файлу для демонстрації...")
        compare_methods("demo-access.log")
    
    # Additional HyperLogLog tests
    print(f"\n{'='*60}")
    print("Додаткові тести HyperLogLog:")
    print(f"{'='*60}")
    
    # Test with different precision values
    test_data = [f"192.168.1.{i}" for i in range(1000)]  # 1000 unique IPs
    actual_unique = len(set(test_data))
    
    print(f"Тестові дані: {len(test_data)} IP-адрес, {actual_unique} унікальних")
    print(f"{'Precision':<10} {'Оцінка':<15} {'Похибка %':<15} {'Пам\'ять (байт)':<15}")
    print("-" * 60)
    
    for precision in [8, 10, 12, 14, 16]:
        hll = HyperLogLog(precision=precision)
        for ip in test_data:
            hll.add(ip)
        
        estimate = hll.estimate_cardinality()
        error = abs(estimate - actual_unique) / actual_unique * 100
        memory = 2 ** precision
        
        print(f"{precision:<10} {estimate:<15.0f} {error:<15.2f} {memory:<15}")
    
    print("\nТести завершено!")
