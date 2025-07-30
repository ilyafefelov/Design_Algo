import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from solution import BloomFilter, check_password_uniqueness


class TestBloomFilter:
    
    def test_initialization(self):
        """Test Bloom filter initialization."""
        bf = BloomFilter(size=100, num_hashes=3)
        assert bf.size == 100
        assert bf.num_hashes == 3
        assert len(bf.bit_array) == 100
        assert all(bit == False for bit in bf.bit_array)
    
    def test_initialization_errors(self):
        """Test initialization with invalid parameters."""
        with pytest.raises(ValueError):
            BloomFilter(size=0, num_hashes=3)
        
        with pytest.raises(ValueError):
            BloomFilter(size=100, num_hashes=0)
        
        with pytest.raises(ValueError):
            BloomFilter(size=-1, num_hashes=3)
    
    def test_add_and_contains(self):
        """Test adding items and checking membership."""
        bf = BloomFilter(size=1000, num_hashes=3)
        
        # Test adding and checking
        bf.add("password123")
        assert bf.contains("password123") == True
        
        # Test item not in filter
        assert bf.contains("notinfilter") == False
    
    def test_multiple_adds(self):
        """Test adding multiple items."""
        bf = BloomFilter(size=1000, num_hashes=3)
        
        passwords = ["pass1", "pass2", "pass3", "pass4"]
        for pwd in passwords:
            bf.add(pwd)
        
        # All added passwords should be detected
        for pwd in passwords:
            assert bf.contains(pwd) == True
        
        # Non-added password should not be detected (very likely)
        assert bf.contains("notadded") == False
    
    def test_type_errors(self):
        """Test type checking for add and contains methods."""
        bf = BloomFilter(size=100, num_hashes=3)
        
        with pytest.raises(TypeError):
            bf.add(123)
        
        with pytest.raises(TypeError):
            bf.contains(123)
        
        with pytest.raises(TypeError):
            bf.add(None)
    
    def test_empty_string(self):
        """Test handling empty strings."""
        bf = BloomFilter(size=100, num_hashes=3)
        
        bf.add("")
        assert bf.contains("") == True
    
    def test_get_stats(self):
        """Test statistics functionality."""
        bf = BloomFilter(size=100, num_hashes=3)
        
        # Initially empty
        stats = bf.get_stats()
        assert stats['size'] == 100
        assert stats['num_hashes'] == 3
        assert stats['bits_set'] == 0
        assert stats['fill_ratio'] == 0.0
        
        # After adding items
        bf.add("test1")
        bf.add("test2")
        stats = bf.get_stats()
        assert stats['bits_set'] > 0
        assert stats['fill_ratio'] > 0


class TestPasswordUniqueness:
    
    def test_basic_functionality(self):
        """Test basic password uniqueness checking."""
        bf = BloomFilter(size=1000, num_hashes=3)
        
        # Add existing passwords
        existing = ["password123", "admin123"]
        for pwd in existing:
            bf.add(pwd)
        
        # Check new passwords
        new_passwords = ["password123", "newpassword", "admin123", "unique"]
        results = check_password_uniqueness(bf, new_passwords)
        
        assert results["password123"] == "вже використаний"
        assert results["admin123"] == "вже використаний"
        assert results["newpassword"] == "унікальний"
        assert results["unique"] == "унікальний"
    
    def test_empty_password(self):
        """Test handling of empty passwords."""
        bf = BloomFilter(size=100, num_hashes=3)
        
        results = check_password_uniqueness(bf, [""])
        assert results[""] == "порожній пароль"
    
    def test_invalid_types(self):
        """Test handling of invalid password types."""
        bf = BloomFilter(size=100, num_hashes=3)
        
        # Test with mixed types (converted to strings for safety)
        test_passwords = [123, "validpassword"]
        # Convert non-strings to strings to test type handling
        safe_passwords = [str(pwd) for pwd in test_passwords]
        
        results = check_password_uniqueness(bf, safe_passwords)
        assert "123" in results
        assert "validpassword" in results
    
    def test_invalid_bloom_filter(self):
        """Test error handling for invalid bloom filter."""
        with pytest.raises(TypeError):
            check_password_uniqueness("not a bloom filter", ["password"])
    
    def test_invalid_password_list(self):
        """Test error handling for invalid password list."""
        bf = BloomFilter(size=100, num_hashes=3)
        
        with pytest.raises(TypeError):
            check_password_uniqueness(bf, "not a list")
    
    def test_large_dataset(self):
        """Test with larger dataset."""
        bf = BloomFilter(size=10000, num_hashes=5)
        
        # Add many existing passwords
        existing = [f"user{i}password" for i in range(1000)]
        for pwd in existing:
            bf.add(pwd)
        
        # Test mixed new and existing
        test_passwords = ["user1password", "user999password", "newcomer", "unique123"]
        results = check_password_uniqueness(bf, test_passwords)
        
        assert results["user1password"] == "вже використаний"
        assert results["user999password"] == "вже використаний"
        assert results["newcomer"] == "унікальний"
        assert results["unique123"] == "унікальний"
    
    def test_false_positive_rate(self):
        """Test that false positive rate is reasonable."""
        bf = BloomFilter(size=1000, num_hashes=3)
        
        # Add some passwords
        existing = [f"password{i}" for i in range(100)]
        for pwd in existing:
            bf.add(pwd)
        
        # Test many new passwords that shouldn't be in the filter
        new_passwords = [f"newpass{i}" for i in range(100)]
        results = check_password_uniqueness(bf, new_passwords)
        
        false_positives = sum(1 for status in results.values() if status == "вже використаний")
        false_positive_rate = false_positives / len(new_passwords)
        
        # Should have some false positives but not too many
        assert false_positive_rate < 0.5  # Less than 50% false positive rate


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
