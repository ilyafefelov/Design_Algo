class TrieNode:
    """Node class for Trie data structure."""
    
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.value = None


class Trie:
    """Basic Trie (prefix tree) implementation."""
    
    def __init__(self):
        self.root = TrieNode()
    
    def put(self, word, value):
        """Insert a word with its value into the Trie."""
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.value = value
    
    def get(self, word):
        """Get value associated with a word."""
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        
        node = self._find_node(word)
        if node and node.is_end_of_word:
            return node.value
        return None
    
    def _find_node(self, prefix):
        """Find the node corresponding to a prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def contains(self, word):
        """Check if word exists in the Trie."""
        if not isinstance(word, str):
            raise TypeError("Word must be a string")
        
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def _get_all_words_from_node(self, node, prefix=""):
        """Helper method to get all words starting from a given node."""
        words = []
        if node.is_end_of_word:
            words.append(prefix)
        
        for char, child_node in node.children.items():
            words.extend(self._get_all_words_from_node(child_node, prefix + char))
        
        return words
    
    def get_all_words(self):
        """Get all words in the Trie."""
        return self._get_all_words_from_node(self.root)
