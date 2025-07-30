"""
Unit tests for Task 1: Sliding Window Rate Limiter

This module contains comprehensive tests for the SlidingWindowRateLimiter class
to ensure all functionality works correctly according to the requirements.
"""

import unittest
import time
from unittest.mock import patch
from task1 import SlidingWindowRateLimiter


class TestSlidingWindowRateLimiter(unittest.TestCase):
    """Test cases for SlidingWindowRateLimiter"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)
    
    def test_first_message_always_allowed(self):
        """Test that the first message from a user is always allowed."""
        # First message should always be allowed
        result = self.limiter.record_message("user1")
        self.assertTrue(result, "First message should always be allowed")
        
        # Different user's first message should also be allowed
        result = self.limiter.record_message("user2")
        self.assertTrue(result, "First message from different user should be allowed")
    
    def test_second_message_blocked_within_window(self):
        """Test that a second message within the window is blocked."""
        # Send first message
        self.limiter.record_message("user1")
        
        # Second message should be blocked
        result = self.limiter.record_message("user1")
        self.assertFalse(result, "Second message within window should be blocked")
    
    def test_can_send_message_without_recording(self):
        """Test can_send_message method without actually recording."""
        # Should be able to send first message
        self.assertTrue(self.limiter.can_send_message("user1"))
        
        # Record a message
        self.limiter.record_message("user1")
        
        # Should not be able to send another immediately
        self.assertFalse(self.limiter.can_send_message("user1"))
    
    def test_cleanup_removes_expired_requests(self):
        """Test that cleanup removes expired requests from the window."""
        with patch('time.time') as mock_time:
            # Start at time 0
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Move to time 5 (within window)
            mock_time.return_value = 5.0
            self.assertFalse(self.limiter.can_send_message("user1"))
            
            # Move to time 11 (outside window)
            mock_time.return_value = 11.0
            self.assertTrue(self.limiter.can_send_message("user1"))
    
    def test_user_removed_when_window_empty(self):
        """Test that user is removed from storage when window becomes empty."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # User should be in the storage
            self.assertIn("user1", self.limiter.user_windows)
            
            # Move beyond window
            mock_time.return_value = 11.0
            self.limiter._cleanup_window("user1", 11.0)
            
            # User should be removed from storage
            self.assertNotIn("user1", self.limiter.user_windows)
    
    def test_time_until_next_allowed(self):
        """Test time_until_next_allowed method."""
        with patch('time.time') as mock_time:
            # Start at time 0
            mock_time.return_value = 0.0
            
            # No message sent yet, should be 0
            self.assertEqual(self.limiter.time_until_next_allowed("user1"), 0.0)
            
            # Send a message
            self.limiter.record_message("user1")
            
            # At time 5, should need to wait 5 more seconds
            mock_time.return_value = 5.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertAlmostEqual(wait_time, 5.0, places=1)
            
            # At time 10, should be able to send (wait time = 0)
            mock_time.return_value = 10.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertEqual(wait_time, 0.0)
    
    def test_multiple_users_independent(self):
        """Test that multiple users are handled independently."""
        # User1 sends a message
        result1 = self.limiter.record_message("user1")
        self.assertTrue(result1)
        
        # User2 should still be able to send (independent)
        result2 = self.limiter.record_message("user2")
        self.assertTrue(result2)
        
        # Both users should now be blocked for second message
        self.assertFalse(self.limiter.can_send_message("user1"))
        self.assertFalse(self.limiter.can_send_message("user2"))
    
    def test_window_size_parameter(self):
        """Test different window sizes."""
        # Create limiter with 5-second window
        short_limiter = SlidingWindowRateLimiter(window_size=5, max_requests=1)
        
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            short_limiter.record_message("user1")
            
            # At time 3, should still be blocked
            mock_time.return_value = 3.0
            self.assertFalse(short_limiter.can_send_message("user1"))
            
            # At time 6, should be able to send
            mock_time.return_value = 6.0
            self.assertTrue(short_limiter.can_send_message("user1"))
    
    def test_max_requests_parameter(self):
        """Test different max_requests values."""
        # Create limiter that allows 2 requests per window
        multi_limiter = SlidingWindowRateLimiter(window_size=10, max_requests=2)
        
        # First two messages should be allowed
        self.assertTrue(multi_limiter.record_message("user1"))
        self.assertTrue(multi_limiter.record_message("user1"))
        
        # Third message should be blocked
        self.assertFalse(multi_limiter.record_message("user1"))
    
    def test_edge_case_zero_wait_time(self):
        """Test edge case where wait time calculation might be negative."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Jump far into the future
            mock_time.return_value = 100.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            
            # Should be 0, not negative
            self.assertEqual(wait_time, 0.0)
    
    def test_cleanup_with_nonexistent_user(self):
        """Test cleanup with a user that doesn't exist."""
        # Should not raise an exception
        try:
            self.limiter._cleanup_window("nonexistent_user", time.time())
        except Exception as e:
            self.fail(f"cleanup_window raised {e} unexpectedly")
    
    def test_concurrent_requests_simulation(self):
        """Test behavior with rapid consecutive requests."""
        with patch('time.time') as mock_time:
            base_time = 1000.0
            
            # Simulate 5 rapid requests from the same user
            results = []
            for i in range(5):
                mock_time.return_value = base_time + (i * 0.1)  # 0.1 second apart
                results.append(self.limiter.record_message("user1"))
            
            # Only the first should succeed
            self.assertEqual(results, [True, False, False, False, False])


class TestSlidingWindowIntegration(unittest.TestCase):
    """Integration tests for the complete sliding window system"""
    
    def test_real_time_behavior(self):
        """Test with actual time delays (integration test)."""
        # Use a very short window for faster testing
        limiter = SlidingWindowRateLimiter(window_size=1, max_requests=1)
        
        # First message should work
        self.assertTrue(limiter.record_message("test_user"))
        
        # Immediate second message should fail
        self.assertFalse(limiter.record_message("test_user"))
        
        # Wait for window to expire
        time.sleep(1.1)
        
        # Should be able to send again
        self.assertTrue(limiter.record_message("test_user"))
    
    def test_stress_test_many_users(self):
        """Stress test with many users."""
        limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)
        
        # Test with 100 different users
        for i in range(100):
            user_id = f"user_{i}"
            # Each user's first message should succeed
            self.assertTrue(limiter.record_message(user_id))
            # Each user's second message should fail
            self.assertFalse(limiter.record_message(user_id))


if __name__ == "__main__":
    unittest.main(verbosity=2)
