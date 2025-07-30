"""
Task 2: Throttling Rate Limiter implementation

This module implements a rate limiter using the Throttling algorithm
to control time intervals between messages by ensuring a fixed waiting
interval between user messages.
"""

import time
from typing import Dict
import random


class ThrottlingRateLimiter:
    """
    Rate limiter implementation using Throttling algorithm.
    
    This class maintains the timestamp of the last message for each user
    and enforces a minimum interval between consecutive messages.
    """
    
    def __init__(self, min_interval: float = 10.0):
        """
        Initialize the Throttling Rate Limiter.
        
        Args:
            min_interval (float): Minimum interval between messages in seconds (default: 10.0)
        """
        self.min_interval = min_interval
        # Dictionary to store the timestamp of the last message for each user
        self.last_message_time: Dict[str, float] = {}
    
    def can_send_message(self, user_id: str) -> bool:
        """
        Check if the user can send a message based on the time of their last message.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            bool: True if the user can send a message, False otherwise
        """
        current_time = time.time()
        
        # If this is the first message from the user, allow it
        if user_id not in self.last_message_time:
            return True
        
        # Check if enough time has passed since the last message
        time_since_last = current_time - self.last_message_time[user_id]
        return time_since_last >= self.min_interval
    
    def record_message(self, user_id: str) -> bool:
        """
        Record a new message with updating the timestamp of the last message.
        
        This method attempts to record a message if the throttling limit allows it.
        
        Args:
            user_id (str): User identifier
            
        Returns:
            bool: True if the message was recorded, False if throttled
        """
        current_time = time.time()
        
        # Check if the user can send a message
        if not self.can_send_message(user_id):
            return False
        
        # Record the timestamp of this message
        self.last_message_time[user_id] = current_time
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
        
        # If this is the first message from the user, they can send now
        if user_id not in self.last_message_time:
            return 0.0
        
        # Calculate time since last message
        time_since_last = current_time - self.last_message_time[user_id]
        
        # If enough time has passed, they can send now
        if time_since_last >= self.min_interval:
            return 0.0
        
        # Calculate remaining wait time
        return self.min_interval - time_since_last
    
    def get_user_stats(self) -> Dict[str, Dict[str, float]]:
        """
        Get statistics for all users (for debugging/monitoring).
        
        Returns:
            Dict containing user statistics
        """
        current_time = time.time()
        stats = {}
        
        for user_id, last_time in self.last_message_time.items():
            time_since_last = current_time - last_time
            time_until_next = max(0.0, self.min_interval - time_since_last)
            
            stats[user_id] = {
                'last_message_time': last_time,
                'time_since_last': time_since_last,
                'time_until_next': time_until_next,
                'can_send': time_since_last >= self.min_interval
            }
        
        return stats


def test_throttling_limiter():
    """
    Demonstration and testing of the Throttling Rate Limiter.
    
    This function simulates a stream of messages from different users
    and shows how the throttling limiter behaves.
    """
    limiter = ThrottlingRateLimiter(min_interval=10.0)
    
    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        
        # Random delay between messages
        time.sleep(random.uniform(0.1, 1.0))
    
    print("\nОчікуємо 10 секунд...")
    time.sleep(10)
    
    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))


def test_edge_cases():
    """Test edge cases and specific scenarios"""
    print("\n=== Тестування граничних випадків (Throttling) ===")
    
    limiter = ThrottlingRateLimiter(min_interval=3.0)
    
    # Test first message for new user
    print("1. Перше повідомлення від нового користувача:")
    result = limiter.record_message("test_user")
    print(f"   Результат: {'✓' if result else '×'}")
    
    # Test immediate second message (should be blocked)
    print("2. Друге повідомлення відразу (має бути заблоковане):")
    result = limiter.record_message("test_user")
    wait_time = limiter.time_until_next_allowed("test_user")
    print(f"   Результат: {'×' if not result else '✓'}, очікування: {wait_time:.1f}с")
    
    # Test after partial wait
    print("3. Очікуємо 2 секунди (недостатньо)...")
    time.sleep(2)
    result = limiter.record_message("test_user")
    wait_time = limiter.time_until_next_allowed("test_user")
    print(f"   Результат: {'×' if not result else '✓'}, очікування: {wait_time:.1f}с")
    
    # Test after full interval
    print("4. Очікуємо ще 2 секунди (всього 4 секунди)...")
    time.sleep(2)
    result = limiter.record_message("test_user")
    print(f"   Результат після повного очікування: {'✓' if result else '×'}")
    
    # Test multiple users
    print("5. Тестування кількох користувачів:")
    for i in range(1, 4):
        result = limiter.record_message(f"user_{i}")
        print(f"   Користувач {i}: {'✓' if result else '×'}")


def demonstrate_algorithm_difference():
    """
    Demonstrate the difference between Throttling and other rate limiting approaches.
    """
    print("\n=== Демонстрація особливостей Throttling ===")
    
    limiter = ThrottlingRateLimiter(min_interval=5.0)
    
    print("Throttling забезпечує фіксований інтервал між повідомленнями:")
    print("- Кожен користувач має свій незалежний таймер")
    print("- Інтервал рахується від останнього успішного повідомлення")
    print("- Не залежить від кількості спроб")
    
    # Demonstrate with rapid attempts
    print("\nРапідні спроби відправки від користувача:")
    for attempt in range(1, 6):
        result = limiter.record_message("rapid_user")
        wait_time = limiter.time_until_next_allowed("rapid_user")
        
        if result:
            print(f"Спроба {attempt}: ✓ Повідомлення відправлено")
        else:
            print(f"Спроба {attempt}: × Заблоковано, очікування {wait_time:.1f}с")
        
        time.sleep(0.5)  # Short delay between attempts


if __name__ == "__main__":
    # Set random seed for reproducible results in demonstration
    random.seed(42)
    
    print("Завдання 2: Throttling Rate Limiter")
    print("=" * 50)
    
    # Run main test
    test_throttling_limiter()
    
    # Run edge case tests
    test_edge_cases()
    
    # Demonstrate algorithm characteristics
    demonstrate_algorithm_difference()
    
    print("\n" + "=" * 50)
    print("Тестування завершено!")
