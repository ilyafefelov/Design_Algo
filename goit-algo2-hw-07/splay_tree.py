"""
Splay Tree implementation for caching Fibonacci numbers
"""

class SplayTreeNode:
    """Node for Splay Tree"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    """
    Splay Tree implementation for efficient caching.
    Automatically moves frequently accessed elements to the root.
    """
    
    def __init__(self):
        self.root = None
    
    def _right_rotate(self, x):
        """Right rotation"""
        y = x.left
        x.left = y.right
        y.right = x
        return y
    
    def _left_rotate(self, x):
        """Left rotation"""
        y = x.right
        x.right = y.left
        y.left = x
        return y
    
    def _splay(self, root, key):
        """
        Splay operation to move the key to root
        
        Args:
            root: Current root
            key: Key to splay
            
        Returns:
            New root after splaying
        """
        if root is None or root.key == key:
            return root
        
        # Key lies in left subtree
        if root.key > key:
            if root.left is None:
                return root
            
            # Zig-Zig (Left Left)
            if root.left.key > key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            
            # Zig-Zag (Left Right)
            elif root.left.key < key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)
            
            if root.left is None:
                return root
            else:
                return self._right_rotate(root)
        
        # Key lies in right subtree
        else:
            if root.right is None:
                return root
            
            # Zag-Zag (Right Right)
            if root.right.key < key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            
            # Zag-Zig (Right Left)
            elif root.right.key > key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)
            
            if root.right is None:
                return root
            else:
                return self._left_rotate(root)
    
    def search(self, key):
        """
        Search for a key in the tree
        
        Args:
            key: Key to search for
            
        Returns:
            Value if found, None otherwise
        """
        self.root = self._splay(self.root, key)
        
        if self.root is not None and self.root.key == key:
            return self.root.value
        return None
    
    def insert(self, key, value):
        """
        Insert a key-value pair into the tree
        
        Args:
            key: Key to insert
            value: Value to insert
        """
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return
        
        self.root = self._splay(self.root, key)
        
        # If key already exists, update value
        if self.root.key == key:
            self.root.value = value
            return
        
        # Create new node
        new_node = SplayTreeNode(key, value)
        
        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node
    
    def get(self, key):
        """
        Get value by key (alias for search)
        
        Args:
            key: Key to search for
            
        Returns:
            Value if found, None otherwise
        """
        return self.search(key)
    
    def put(self, key, value):
        """
        Put key-value pair (alias for insert)
        
        Args:
            key: Key to insert
            value: Value to insert
        """
        self.insert(key, value)
