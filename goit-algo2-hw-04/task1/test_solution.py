import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solution import Homework

class TestHomework:
    
    def setup_method(self):
        """Set up test data before each test method."""
        self.trie = Homework()
        words = ["apple", "application", "banana", "cat", "car", "card", "care", "careful"]
        for i, word in enumerate(words):
            self.trie.put(word, i)
    
    def test_count_words_with_suffix_basic(self):
        """Test basic functionality of count_words_with_suffix."""
        assert self.trie.count_words_with_suffix("e") == 2  # apple, care
        assert self.trie.count_words_with_suffix("ion") == 1  # application
        assert self.trie.count_words_with_suffix("a") == 1  # banana
        assert self.trie.count_words_with_suffix("at") == 1  # cat
        assert self.trie.count_words_with_suffix("ar") == 1  # car
        assert self.trie.count_words_with_suffix("ful") == 1  # careful
    
    def test_count_words_with_suffix_case_sensitive(self):
        """Test that suffix matching is case sensitive."""
        self.trie.put("Apple", 10)
        assert self.trie.count_words_with_suffix("e") == 3  # apple, care, Apple
        assert self.trie.count_words_with_suffix("E") == 0  # no words end with capital E
    
    def test_count_words_with_suffix_no_matches(self):
        """Test suffix counting when no words match."""
        assert self.trie.count_words_with_suffix("xyz") == 0
        assert self.trie.count_words_with_suffix("zz") == 0
    
    def test_count_words_with_suffix_error_handling(self):
        """Test error handling for count_words_with_suffix."""
        with pytest.raises(TypeError):
            self.trie.count_words_with_suffix(123)
        
        with pytest.raises(TypeError):
            self.trie.count_words_with_suffix(None)
        
        with pytest.raises(ValueError):
            self.trie.count_words_with_suffix("")
    
    def test_has_prefix_basic(self):
        """Test basic functionality of has_prefix."""
        assert self.trie.has_prefix("app") == True  # apple, application
        assert self.trie.has_prefix("car") == True  # car, card, care, careful
        assert self.trie.has_prefix("ban") == True  # banana
        assert self.trie.has_prefix("ca") == True  # cat, car, card, care, careful
        assert self.trie.has_prefix("bat") == False
    
    def test_has_prefix_exact_word(self):
        """Test has_prefix with exact words."""
        assert self.trie.has_prefix("cat") == True  # exact word
        assert self.trie.has_prefix("car") == True  # exact word with extensions
        assert self.trie.has_prefix("apple") == True  # exact word
    
    def test_has_prefix_case_sensitive(self):
        """Test that prefix matching is case sensitive."""
        assert self.trie.has_prefix("App") == False  # no words start with capital A
        assert self.trie.has_prefix("CAR") == False  # no words start with capitals
    
    def test_has_prefix_no_matches(self):
        """Test prefix checking when no words match."""
        assert self.trie.has_prefix("xyz") == False
        assert self.trie.has_prefix("dog") == False
    
    def test_has_prefix_error_handling(self):
        """Test error handling for has_prefix."""
        with pytest.raises(TypeError):
            self.trie.has_prefix(123)
        
        with pytest.raises(TypeError):
            self.trie.has_prefix(None)
        
        with pytest.raises(ValueError):
            self.trie.has_prefix("")
    
    def test_empty_trie(self):
        """Test methods on empty trie."""
        empty_trie = Homework()
        assert empty_trie.count_words_with_suffix("test") == 0
        assert empty_trie.has_prefix("test") == False
    
    def test_single_character_operations(self):
        """Test operations with single characters."""
        assert self.trie.count_words_with_suffix("t") == 1  # cat
        assert self.trie.has_prefix("c") == True  # cat, car, card, care, careful
        assert self.trie.has_prefix("b") == True  # banana
        assert self.trie.has_prefix("a") == True  # apple, application


if __name__ == "__main__":
    pytest.main([__file__])
