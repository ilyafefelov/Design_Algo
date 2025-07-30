import hashlib
from typing import List, Dict


class BloomFilter:
    """
    Bloom Filter implementation for efficient membership testing.
    
    A Bloom filter is a space-efficient probabilistic data structure
    that is used to test whether an element is a member of a set.
    False positive matches are possible, but false negatives are not.
    """
    
    def __init__(self, size: int, num_hashes: int):
        """
        Initialize the Bloom filter.
        
        Args:
            size (int): Size of the bit array
            num_hashes (int): Number of hash functions to use
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer")
        if num_hashes <= 0:
            raise ValueError("Number of hashes must be a positive integer")
            
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size
    
    def _hash(self, item: str, seed: int) -> int:
        """
        Generate hash for an item using a specific seed.
        
        Args:
            item (str): Item to hash
            seed (int): Seed for the hash function
            
        Returns:
            int: Hash value modulo the size of the bit array
        """
        # Combine item and seed for different hash functions
        hash_input = f"{item}_{seed}".encode('utf-8')
        hash_obj = hashlib.md5(hash_input)
        return int(hash_obj.hexdigest(), 16) % self.size
    
    def add(self, item: str) -> None:
        """
        Add an item to the Bloom filter.
        
        Args:
            item (str): Item to add to the filter
        """
        if not isinstance(item, str):
            raise TypeError("Item must be a string")
        
        # Set bits for all hash functions
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            self.bit_array[index] = True
    
    def contains(self, item: str) -> bool:
        """
        Check if an item might be in the set.
        
        Args:
            item (str): Item to check
            
        Returns:
            bool: True if item might be in the set (could be false positive),
                  False if item is definitely not in the set
        """
        if not isinstance(item, str):
            raise TypeError("Item must be a string")
        
        # Check all hash functions
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def get_stats(self) -> Dict[str, float]:
        """
        Get statistics about the Bloom filter.
        
        Returns:
            Dict[str, float]: Dictionary with filter statistics
        """
        bits_set = sum(self.bit_array)
        fill_ratio = bits_set / self.size
        # Approximate false positive probability
        false_positive_prob = (1 - (1 - fill_ratio) ** self.num_hashes)
        
        return {
            'size': self.size,
            'num_hashes': self.num_hashes,
            'bits_set': bits_set,
            'fill_ratio': fill_ratio,
            'estimated_false_positive_rate': false_positive_prob
        }


def check_password_uniqueness(bloom_filter: BloomFilter, new_passwords: List[str]) -> Dict[str, str]:
    """
    Check the uniqueness of new passwords using a Bloom filter.
    
    Args:
        bloom_filter (BloomFilter): Pre-configured Bloom filter with existing passwords
        new_passwords (List[str]): List of new passwords to check
        
    Returns:
        Dict[str, str]: Dictionary mapping passwords to their status
                       ("унікальний" or "вже використаний")
    """
    if not isinstance(bloom_filter, BloomFilter):
        raise TypeError("bloom_filter must be an instance of BloomFilter")
    
    if not isinstance(new_passwords, list):
        raise TypeError("new_passwords must be a list")
    
    results = {}
    
    for password in new_passwords:
        # Handle non-string passwords
        if not isinstance(password, str):
            results[str(password)] = "некоректний тип даних"
            continue
        
        # Handle empty passwords
        if not password:
            results[password] = "порожній пароль"
            continue
        
        # Check if password might already exist
        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
    
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    print("Результати перевірки паролів:")
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
    
    # Додаткові тести
    print("\n" + "="*50)
    print("Додаткові тести:")
    
    # Тест з більшою кількістю паролів
    print("\nТест з великою кількістю паролів:")
    large_bloom = BloomFilter(size=10000, num_hashes=5)
    
    # Додаємо багато існуючих паролів
    existing_large = [f"password{i}" for i in range(1000)]
    for pwd in existing_large:
        large_bloom.add(pwd)
    
    # Перевіряємо нові
    test_passwords = ["password1", "password999", "newpassword1", "uniquepass"]
    results_large = check_password_uniqueness(large_bloom, test_passwords)
    
    for password, status in results_large.items():
        print(f"Пароль '{password}' - {status}.")
    
    # Показуємо статистику фільтра
    print(f"\nСтатистика фільтра:")
    stats = large_bloom.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value:.4f}")
    
    # Тест обробки помилок
    print("\nТест обробки помилок:")
    error_test_passwords = ["", 123, None, "validpassword"]
    try:
        # Створюємо список для тестування (замінюємо None на строку для безпеки)
        safe_test_passwords = []
        for pwd in error_test_passwords:
            if pwd is None:
                safe_test_passwords.append("None")
            else:
                safe_test_passwords.append(pwd)
        
        error_results = check_password_uniqueness(bloom, safe_test_passwords)
        for password, status in error_results.items():
            print(f"Тест '{password}' - {status}.")
    except Exception as e:
        print(f"Помилка: {e}")
    
    print("\nВсі тести завершено!")
