"""
LRU Cache implementation for optimizing data access
"""

class LRUCache:
    """
    Least Recently Used (LRU) Cache implementation using a doubly linked list
    and hash map for O(1) operations.
    """
    
    class Node:
        def __init__(self, key=0, value=0):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None
    
    def __init__(self, capacity: int):
        """
        Initialize LRU Cache with given capacity
        
        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # key -> node
        
        # Create dummy head and tail nodes
        self.head = self.Node()
        self.tail = self.Node()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node):
        """Add node right after head"""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """Remove an existing node from the linked list"""
        prev_node = node.prev
        new_node = node.next
        
        prev_node.next = new_node
        new_node.prev = prev_node
    
    def _move_to_head(self, node):
        """Move certain node to head"""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """Pop the current tail"""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key):
        """
        Get value by key. Returns -1 if key doesn't exist.
        
        Args:
            key: Key to search for
            
        Returns:
            Value if key exists, -1 otherwise
        """
        node = self.cache.get(key)
        
        if not node:
            return -1
        
        # Move the accessed node to the head
        self._move_to_head(node)
        
        return node.value
    
    def put(self, key, value):
        """
        Put key-value pair into cache
        
        Args:
            key: Key to store
            value: Value to store
        """
        node = self.cache.get(key)
        
        if not node:
            new_node = self.Node(key, value)
            
            self.cache[key] = new_node
            self._add_node(new_node)
            
            if len(self.cache) > self.capacity:
                # Pop the tail
                tail = self._pop_tail()
                del self.cache[tail.key]
        else:
            # Update the value
            node.value = value
            self._move_to_head(node)
    
    def keys(self):
        """Return all keys in the cache"""
        return list(self.cache.keys())
    
    def remove(self, key):
        """
        Remove key from cache if it exists
        
        Args:
            key: Key to remove
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
    
    def clear(self):
        """Clear all items from cache"""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def size(self):
        """Return current cache size"""
        return len(self.cache)
