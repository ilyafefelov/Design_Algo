"""
Task 1: Sliding Window Rate Limiter implementation

This module implements a rate limiter using the Sliding Window algorithm
to precisely control time intervals and track the number of messages
within a given time window.
"""

import random
from typing import Dict
import time
from collections import deque


class SlidingWindowRateLimiter:
    """
    Rate limiter implementation using Sliding Window algorithm.
    
    This class maintains a sliding window of timestamps for each user
    and enforces rate limits based on the number of requests within
    the time window.
    """
    
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        """
        Initialize the Sliding Window Rate Limiter.
        
        Args:
            window_size (int): Size of the time window in seconds (default: 10)
            max_requests (int): Maximum number of requests allowed in the window (default: 1)
        """
        self.window_size = window_size
        self.max_requests = max_requests
        # Dictionary to store deque of timestamps for each user
        self.user_windows: Dict[str, deque] = {}
    
    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """
        Clean up expired requests from the user's window.
        
        This method removes all timestamps that are older than the window size
        and removes the user entry if no active timestamps remain.
        
        Args:
            user_id (str): User identifier
            current_time (float): Current timestamp
        """
        if user_id not in self.user_windows:
            return
        
        user_window = self.user_windows[user_id]
        cutoff_time = current_time - self.window_size
        
        # Remove timestamps older than the window
        while user_window and user_window[0] <= cutoff_time:
            user_window.popleft()
        
        # Remove user entry if no active timestamps remain
        if not user_window:
            del self.user_windows[user_id]
    
    def can_send_message(self, user_id: str) -> bool:
        """
        Check if the user can send a message in the current time window.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            bool: True if the user can send a message, False otherwise
        """
        current_time = time.time()
        
        # Clean up expired entries first
        self._cleanup_window(user_id, current_time)
        
        # If user has no active window, they can send
        if user_id not in self.user_windows:
            return True
        
        # Check if the number of requests is below the limit
        return len(self.user_windows[user_id]) < self.max_requests
    
    def record_message(self, user_id: str) -> bool:
        """
        Record a new message and update the user's history.
        
        This method attempts to record a message if the rate limit allows it.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            bool: True if the message was recorded, False if rate limited
        """
        current_time = time.time()
        
        # Check if the user can send a message
        if not self.can_send_message(user_id):
            return False
        
        # Initialize user window if it doesn't exist
        if user_id not in self.user_windows:
            self.user_windows[user_id] = deque()
        
        # Record the message timestamp
        self.user_windows[user_id].append(current_time)
        
        return True
    
    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Calculate the time until the next message is allowed.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            float: Time in seconds until the next message is allowed (0 if can send now)
        """
        current_time = time.time()
        
        # Clean up expired entries
        self._cleanup_window(user_id, current_time)
        
        # If user has no active window or is below limit, they can send now
        if user_id not in self.user_windows:
            return 0.0
        
        user_window = self.user_windows[user_id]
        
        # If below limit, can send now
        if len(user_window) < self.max_requests:
            return 0.0
        
        # Calculate time until oldest request expires
        oldest_request = user_window[0]
        time_until_expire = (oldest_request + self.window_size) - current_time
        
        return max(0.0, time_until_expire)


def test_rate_limiter():
    """
    Demonstration and testing of the Sliding Window Rate Limiter.
    
    This function simulates a stream of messages from different users
    and shows how the rate limiter behaves.
    """
    # Create rate limiter: 10-second window, 1 message max
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)
    
    # Simulate message flow from users (sequential IDs from 1 to 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        # Simulate different users (IDs from 1 to 5)
        user_id = message_id % 5 + 1
        
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        
        # Small delay between messages for realism
        # Random delay from 0.1 to 1 second
        time.sleep(random.uniform(0.1, 1.0))
    
    # Wait for window to clear
    print("\nОчікуємо 4 секунди...")
    time.sleep(4)
    
    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        # Random delay from 0.1 to 1 second
        time.sleep(random.uniform(0.1, 1.0))


def test_edge_cases():
    """Test edge cases and specific scenarios"""
    print("\n=== Тестування граничних випадків ===")
    
    limiter = SlidingWindowRateLimiter(window_size=5, max_requests=2)
    
    # Test first message for new user
    print("1. Перше повідомлення від нового користувача:")
    result = limiter.record_message("test_user")
    print(f"   Результат: {'✓' if result else '×'}")
    
    # Test immediate second message
    print("2. Друге повідомлення відразу:")
    result = limiter.record_message("test_user")
    print(f"   Результат: {'✓' if result else '×'}")
    
    # Test third message (should be blocked)
    print("3. Третє повідомлення (має бути заблоковане):")
    result = limiter.record_message("test_user")
    wait_time = limiter.time_until_next_allowed("test_user")
    print(f"   Результат: {'×' if not result else '✓'}, очікування: {wait_time:.1f}с")
    
    # Test after window expiry
    print("4. Очікуємо 6 секунд для закінчення вікна...")
    time.sleep(6)
    result = limiter.record_message("test_user")
    print(f"   Результат після очікування: {'✓' if result else '×'}")


if __name__ == "__main__":
    # Set random seed for reproducible results in demonstration
    random.seed(42)
    
    print("Завдання 1: Sliding Window Rate Limiter")
    print("=" * 50)
    
    # Run main test
    test_rate_limiter()
    
    # Run edge case tests
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("Тестування завершено!")
