import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trie import Trie

class LongestCommonWord(Trie):
    
    def find_longest_common_word(self, strings) -> str:
        """
        Find the longest common prefix for all strings in the input array.
        
        Args:
            strings: List of strings to find common prefix for
            
        Returns:
            str: The longest common prefix, or empty string if no common prefix exists
            
        Raises:
            TypeError: If strings is not a list or contains non-string elements
        """
        # Input validation
        if not isinstance(strings, list):
            raise TypeError("Input must be a list of strings")
        
        if not strings:
            return ""
        
        # Check that all elements are strings
        for i, s in enumerate(strings):
            if not isinstance(s, str):
                raise TypeError(f"Element at index {i} is not a string")
        
        # Handle empty strings
        if any(s == "" for s in strings):
            return ""
        
        # Clear the trie and insert all strings
        self.root = Trie().root
        for string in strings:
            self.put(string, True)
        
        # Traverse the trie to find the longest common prefix
        result = ""
        current_node = self.root
        
        while True:
            # If current node has more than one child, or is end of word, stop
            if len(current_node.children) != 1 or current_node.is_end_of_word:
                break
            
            # Get the single child
            char = next(iter(current_node.children.keys()))
            result += char
            current_node = current_node.children[char]
        
        return result


if __name__ == "__main__":
    # Тести
    print("Testing find_longest_common_word:")
    
    trie = LongestCommonWord()
    strings = ["flower", "flow", "flight"]
    result = trie.find_longest_common_word(strings)
    print(f"Common prefix of {strings}: '{result}'")
    assert result == "fl"

    trie = LongestCommonWord()
    strings = ["interspecies", "interstellar", "interstate"]
    result = trie.find_longest_common_word(strings)
    print(f"Common prefix of {strings}: '{result}'")
    assert result == "inters"

    trie = LongestCommonWord()
    strings = ["dog", "racecar", "car"]
    result = trie.find_longest_common_word(strings)
    print(f"Common prefix of {strings}: '{result}'")
    assert result == ""
    
    print("\nAll basic tests passed!")
    
    # Additional edge case tests
    print("\nTesting edge cases:")
    
    # Test with empty list
    trie = LongestCommonWord()
    result = trie.find_longest_common_word([])
    print(f"Empty list result: '{result}'")
    assert result == ""
    
    # Test with single string
    trie = LongestCommonWord()
    result = trie.find_longest_common_word(["hello"])
    print(f"Single string result: '{result}'")
    assert result == "hello"
    
    # Test with identical strings
    trie = LongestCommonWord()
    result = trie.find_longest_common_word(["test", "test", "test"])
    print(f"Identical strings result: '{result}'")
    assert result == "test"
    
    # Test with empty string in list
    trie = LongestCommonWord()
    result = trie.find_longest_common_word(["hello", "", "help"])
    print(f"Empty string in list result: '{result}'")
    assert result == ""
    
    # Test with no common prefix
    trie = LongestCommonWord()
    result = trie.find_longest_common_word(["abc", "def", "ghi"])
    print(f"No common prefix result: '{result}'")
    assert result == ""
    
    # Test with one string being prefix of another
    trie = LongestCommonWord()
    result = trie.find_longest_common_word(["test", "testing", "tester"])
    print(f"Prefix relationship result: '{result}'")
    assert result == "test"
    
    # Test error handling
    try:
        trie.find_longest_common_word("not a list")
        assert False, "Should raise TypeError"
    except TypeError:
        print("TypeError handling for non-list input works")
    
    try:
        trie.find_longest_common_word(["string", 123, "another"])
        assert False, "Should raise TypeError"
    except TypeError:
        print("TypeError handling for non-string elements works")
    
    print("\nAll edge case tests passed!")
    print("All tests completed successfully!")
