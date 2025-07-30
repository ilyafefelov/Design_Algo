"""
Unit tests for Task 2: Throttling Rate Limiter

This module contains comprehensive tests for the ThrottlingRateLimiter class
to ensure all functionality works correctly according to the requirements.
"""

import unittest
import time
from unittest.mock import patch
from task2 import ThrottlingRateLimiter


class TestThrottlingRateLimiter(unittest.TestCase):
    """Test cases for ThrottlingRateLimiter"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.limiter = ThrottlingRateLimiter(min_interval=10.0)
    
    def test_first_message_always_allowed(self):
        """Test that the first message from a user is always allowed."""
        # First message should always be allowed
        result = self.limiter.record_message("user1")
        self.assertTrue(result, "First message should always be allowed")
        
        # Different user's first message should also be allowed
        result = self.limiter.record_message("user2")
        self.assertTrue(result, "First message from different user should be allowed")
    
    def test_second_message_blocked_before_interval(self):
        """Test that a second message before the interval is blocked."""
        with patch('time.time') as mock_time:
            # Send first message at time 0
            mock_time.return_value = 0.0
            result = self.limiter.record_message("user1")
            self.assertTrue(result)
            
            # Try to send second message at time 5 (before 10-second interval)
            mock_time.return_value = 5.0
            result = self.limiter.record_message("user1")
            self.assertFalse(result, "Second message before interval should be blocked")
    
    def test_second_message_allowed_after_interval(self):
        """Test that a second message after the interval is allowed."""
        with patch('time.time') as mock_time:
            # Send first message at time 0
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Send second message at time 10 (exactly at interval)
            mock_time.return_value = 10.0
            result = self.limiter.record_message("user1")
            self.assertTrue(result, "Second message after interval should be allowed")
    
    def test_can_send_message_without_recording(self):
        """Test can_send_message method without actually recording."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            
            # Should be able to send first message
            self.assertTrue(self.limiter.can_send_message("user1"))
            
            # Record a message
            self.limiter.record_message("user1")
            
            # Should not be able to send another immediately
            mock_time.return_value = 5.0
            self.assertFalse(self.limiter.can_send_message("user1"))
            
            # Should be able to send after interval
            mock_time.return_value = 10.0
            self.assertTrue(self.limiter.can_send_message("user1"))
    
    def test_time_until_next_allowed_new_user(self):
        """Test time_until_next_allowed for new user."""
        # New user should have 0 wait time
        wait_time = self.limiter.time_until_next_allowed("new_user")
        self.assertEqual(wait_time, 0.0)
    
    def test_time_until_next_allowed_calculation(self):
        """Test time_until_next_allowed calculation."""
        with patch('time.time') as mock_time:
            # Send message at time 0
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # At time 3, should need to wait 7 more seconds
            mock_time.return_value = 3.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertAlmostEqual(wait_time, 7.0, places=1)
            
            # At time 8, should need to wait 2 more seconds
            mock_time.return_value = 8.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertAlmostEqual(wait_time, 2.0, places=1)
            
            # At time 10, should be able to send (wait time = 0)
            mock_time.return_value = 10.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertEqual(wait_time, 0.0)
            
            # At time 15, should still be 0 (past the interval)
            mock_time.return_value = 15.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertEqual(wait_time, 0.0)
    
    def test_multiple_users_independent(self):
        """Test that multiple users are handled independently."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            
            # User1 sends a message
            result1 = self.limiter.record_message("user1")
            self.assertTrue(result1)
            
            # User2 should still be able to send (independent)
            result2 = self.limiter.record_message("user2")
            self.assertTrue(result2)
            
            # Move time forward 5 seconds
            mock_time.return_value = 5.0
            
            # Both users should be blocked for second message
            self.assertFalse(self.limiter.can_send_message("user1"))
            self.assertFalse(self.limiter.can_send_message("user2"))
            
            # User1 sends at time 10 (allowed)
            mock_time.return_value = 10.0
            self.assertTrue(self.limiter.can_send_message("user1"))
            
            # User2 should also be allowed at time 10
            self.assertTrue(self.limiter.can_send_message("user2"))
    
    def test_min_interval_parameter(self):
        """Test different min_interval values."""
        # Create limiter with 5-second interval
        short_limiter = ThrottlingRateLimiter(min_interval=5.0)
        
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            short_limiter.record_message("user1")
            
            # At time 3, should still be blocked
            mock_time.return_value = 3.0
            self.assertFalse(short_limiter.can_send_message("user1"))
            
            # At time 5, should be able to send
            mock_time.return_value = 5.0
            self.assertTrue(short_limiter.can_send_message("user1"))
    
    def test_record_message_updates_timestamp(self):
        """Test that record_message properly updates the timestamp."""
        with patch('time.time') as mock_time:
            # Record first message at time 0
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Move to time 10 and record second message
            mock_time.return_value = 10.0
            self.limiter.record_message("user1")
            
            # Now the last message time should be 10, not 0
            # So at time 15, user should still need to wait 5 seconds
            mock_time.return_value = 15.0
            wait_time = self.limiter.time_until_next_allowed("user1")
            self.assertAlmostEqual(wait_time, 5.0, places=1)
    
    def test_edge_case_exact_interval_timing(self):
        """Test edge case where message is sent exactly at interval."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Exactly at the interval
            mock_time.return_value = 10.0
            self.assertTrue(self.limiter.can_send_message("user1"))
            
            # Just before the interval
            mock_time.return_value = 9.999
            self.assertFalse(self.limiter.can_send_message("user1"))
            
            # Just after the interval
            mock_time.return_value = 10.001
            self.assertTrue(self.limiter.can_send_message("user1"))
    
    def test_get_user_stats(self):
        """Test the get_user_stats method."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            self.limiter.record_message("user2")
            
            mock_time.return_value = 5.0
            stats = self.limiter.get_user_stats()
            
            # Should have stats for both users
            self.assertIn("user1", stats)
            self.assertIn("user2", stats)
            
            # Check user1 stats
            user1_stats = stats["user1"]
            self.assertEqual(user1_stats["last_message_time"], 0.0)
            self.assertEqual(user1_stats["time_since_last"], 5.0)
            self.assertEqual(user1_stats["time_until_next"], 5.0)
            self.assertFalse(user1_stats["can_send"])
    
    def test_failed_record_does_not_update_timestamp(self):
        """Test that failed record_message doesn't update timestamp."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Failed attempt at time 5
            mock_time.return_value = 5.0
            result = self.limiter.record_message("user1")
            self.assertFalse(result)
            
            # Timestamp should still be 0, not 5
            # So at time 10, user should be able to send
            mock_time.return_value = 10.0
            self.assertTrue(self.limiter.can_send_message("user1"))
    
    def test_multiple_failed_attempts(self):
        """Test multiple failed attempts don't affect timing."""
        with patch('time.time') as mock_time:
            mock_time.return_value = 0.0
            self.limiter.record_message("user1")
            
            # Multiple failed attempts
            for t in [1, 2, 3, 4, 5]:
                mock_time.return_value = t
                result = self.limiter.record_message("user1")
                self.assertFalse(result)
            
            # Should still be based on original timestamp (0)
            mock_time.return_value = 10.0
            self.assertTrue(self.limiter.can_send_message("user1"))


class TestThrottlingIntegration(unittest.TestCase):
    """Integration tests for the complete throttling system"""
    
    def test_real_time_behavior(self):
        """Test with actual time delays (integration test)."""
        # Use a very short interval for faster testing
        limiter = ThrottlingRateLimiter(min_interval=1.0)
        
        # First message should work
        self.assertTrue(limiter.record_message("test_user"))
        
        # Immediate second message should fail
        self.assertFalse(limiter.record_message("test_user"))
        
        # Wait for interval to pass
        time.sleep(1.1)
        
        # Should be able to send again
        self.assertTrue(limiter.record_message("test_user"))
    
    def test_stress_test_many_users(self):
        """Stress test with many users."""
        limiter = ThrottlingRateLimiter(min_interval=10.0)
        
        # Test with 100 different users
        for i in range(100):
            user_id = f"user_{i}"
            # Each user's first message should succeed
            self.assertTrue(limiter.record_message(user_id))
            # Each user's second message should fail
            self.assertFalse(limiter.record_message(user_id))
    
    def test_rapid_fire_attempts(self):
        """Test rapid-fire attempts from the same user."""
        limiter = ThrottlingRateLimiter(min_interval=5.0)
        
        # First message succeeds
        self.assertTrue(limiter.record_message("rapid_user"))
        
        # 10 rapid attempts should all fail
        for _ in range(10):
            self.assertFalse(limiter.record_message("rapid_user"))
            time.sleep(0.1)  # Very short delay
        
        # After waiting, should succeed
        time.sleep(5.0)
        self.assertTrue(limiter.record_message("rapid_user"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
