import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trie import Trie

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        """
        Count the number of words that end with the given pattern.
        
        Args:
            pattern (str): The suffix pattern to search for
            
        Returns:
            int: Number of words ending with the pattern
            
        Raises:
            TypeError: If pattern is not a string
            ValueError: If pattern is empty
        """
        # Input validation
        if not isinstance(pattern, str):
            raise TypeError("Pattern must be a string")
        
        if not pattern:
            raise ValueError("Pattern cannot be empty")
        
        # Get all words from the Trie
        all_words = self.get_all_words()
        
        # Count words that end with the pattern
        count = 0
        for word in all_words:
            if word.endswith(pattern):
                count += 1
        
        return count

    def has_prefix(self, prefix) -> bool:
        """
        Check if there exists at least one word with the given prefix.
        
        Args:
            prefix (str): The prefix to search for
            
        Returns:
            bool: True if at least one word has the prefix, False otherwise
            
        Raises:
            TypeError: If prefix is not a string
            ValueError: If prefix is empty
        """
        # Input validation
        if not isinstance(prefix, str):
            raise TypeError("Prefix must be a string")
        
        if not prefix:
            raise ValueError("Prefix cannot be empty")
        
        # Find the node corresponding to the prefix
        node = self._find_node(prefix)
        
        # If node exists, check if there are any words with this prefix
        if node is None:
            return False
        
        # Check if this node itself is end of word or has any children
        return node.is_end_of_word or bool(node.children)


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    print("Testing count_words_with_suffix:")
    print(f"Words ending with 'e': {trie.count_words_with_suffix('e')}")  # Should be 1 (apple)
    print(f"Words ending with 'ion': {trie.count_words_with_suffix('ion')}")  # Should be 1 (application)
    print(f"Words ending with 'a': {trie.count_words_with_suffix('a')}")  # Should be 1 (banana)
    print(f"Words ending with 'at': {trie.count_words_with_suffix('at')}")  # Should be 1 (cat)
    
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    print("\nTesting has_prefix:")
    print(f"Has prefix 'app': {trie.has_prefix('app')}")  # Should be True (apple, application)
    print(f"Has prefix 'bat': {trie.has_prefix('bat')}")  # Should be False
    print(f"Has prefix 'ban': {trie.has_prefix('ban')}")  # Should be True (banana)
    print(f"Has prefix 'ca': {trie.has_prefix('ca')}")  # Should be True (cat)
    
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
    
    print("\nAll tests passed!")
    
    # Additional tests for edge cases
    print("\nTesting edge cases:")
    
    # Test with non-existent suffixes
    assert trie.count_words_with_suffix("xyz") == 0
    print("Non-existent suffix test passed")
    
    # Test with non-existent prefixes
    assert trie.has_prefix("xyz") == False
    print("Non-existent prefix test passed")
    
    # Test error handling
    try:
        trie.count_words_with_suffix(123)
        assert False, "Should raise TypeError"
    except TypeError:
        print("TypeError handling for count_words_with_suffix works")
    
    try:
        trie.has_prefix(123)
        assert False, "Should raise TypeError"
    except TypeError:
        print("TypeError handling for has_prefix works")
    
    try:
        trie.count_words_with_suffix("")
        assert False, "Should raise ValueError"
    except ValueError:
        print("ValueError handling for empty pattern works")
    
    try:
        trie.has_prefix("")
        assert False, "Should raise ValueError"
    except ValueError:
        print("ValueError handling for empty prefix works")
    
    print("\nAll edge case tests passed!")
