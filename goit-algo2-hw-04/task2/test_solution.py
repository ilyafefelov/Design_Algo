import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solution import LongestCommonWord

class TestLongestCommonWord:
    
    def test_basic_functionality(self):
        """Test basic functionality with provided examples."""
        trie = LongestCommonWord()
        
        # Test case 1
        strings = ["flower", "flow", "flight"]
        assert trie.find_longest_common_word(strings) == "fl"
        
        # Test case 2
        trie = LongestCommonWord()
        strings = ["interspecies", "interstellar", "interstate"]
        assert trie.find_longest_common_word(strings) == "inters"
        
        # Test case 3
        trie = LongestCommonWord()
        strings = ["dog", "racecar", "car"]
        assert trie.find_longest_common_word(strings) == ""
    
    def test_empty_input(self):
        """Test with empty input."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word([]) == ""
    
    def test_single_string(self):
        """Test with single string."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["hello"]) == "hello"
        assert trie.find_longest_common_word(["a"]) == "a"
        assert trie.find_longest_common_word([""]) == ""
    
    def test_identical_strings(self):
        """Test with identical strings."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["test", "test", "test"]) == "test"
        assert trie.find_longest_common_word(["", "", ""]) == ""
    
    def test_no_common_prefix(self):
        """Test cases with no common prefix."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["abc", "def", "ghi"]) == ""
        assert trie.find_longest_common_word(["hello", "world", "python"]) == ""
        assert trie.find_longest_common_word(["a", "b", "c"]) == ""
    
    def test_empty_string_in_list(self):
        """Test with empty string in the list."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["hello", "", "help"]) == ""
        assert trie.find_longest_common_word(["", "test"]) == ""
        assert trie.find_longest_common_word(["test", ""]) == ""
    
    def test_prefix_relationships(self):
        """Test cases where one string is prefix of another."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["test", "testing", "tester"]) == "test"
        assert trie.find_longest_common_word(["a", "ab", "abc"]) == "a"
        assert trie.find_longest_common_word(["hello", "helloworld"]) == "hello"
    
    def test_case_sensitivity(self):
        """Test case sensitivity."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["Hello", "hello"]) == ""
        assert trie.find_longest_common_word(["Test", "test", "TEST"]) == ""
        assert trie.find_longest_common_word(["abc", "ABC"]) == ""
    
    def test_special_characters(self):
        """Test with special characters."""
        trie = LongestCommonWord()
        assert trie.find_longest_common_word(["test@email.com", "test@domain.org"]) == "test@"
        assert trie.find_longest_common_word(["hello-world", "hello-there"]) == "hello-"
        assert trie.find_longest_common_word(["123abc", "123def"]) == "123"
    
    def test_long_common_prefix(self):
        """Test with long common prefixes."""
        trie = LongestCommonWord()
        strings = [
            "verylongcommonprefix_variant1",
            "verylongcommonprefix_variant2", 
            "verylongcommonprefix_variant3"
        ]
        assert trie.find_longest_common_word(strings) == "verylongcommonprefix_variant"
    
    def test_error_handling(self):
        """Test error handling."""
        trie = LongestCommonWord()
        
        # Test with non-list input
        with pytest.raises(TypeError):
            trie.find_longest_common_word("not a list")
        
        with pytest.raises(TypeError):
            trie.find_longest_common_word(123)
        
        with pytest.raises(TypeError):
            trie.find_longest_common_word(None)
        
        # Test with non-string elements
        with pytest.raises(TypeError):
            trie.find_longest_common_word(["string", 123, "another"])
        
        with pytest.raises(TypeError):
            trie.find_longest_common_word(["string", None, "another"])
        
        with pytest.raises(TypeError):
            trie.find_longest_common_word(["string", ["nested", "list"]])
    
    def test_performance_with_large_data(self):
        """Test performance with larger datasets."""
        trie = LongestCommonWord()
        
        # Create strings with common prefix
        strings = [f"commonprefix{i}" for i in range(100)]
        assert trie.find_longest_common_word(strings) == "commonprefix"
        
        # Create strings with no common prefix
        strings = [f"different{i}prefix{i}" for i in range(50)]
        result = trie.find_longest_common_word(strings)
        # All start with 'd' so common prefix should be 'd'
        assert result == "different"


if __name__ == "__main__":
    pytest.main([__file__])
