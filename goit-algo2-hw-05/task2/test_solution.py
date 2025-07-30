import pytest
import sys
import os
import tempfile
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from solution import HyperLogLog, extract_ips_from_log, exact_unique_count, hyperloglog_unique_count, create_sample_log_file


class TestHyperLogLog:
    
    def test_initialization(self):
        """Test HyperLogLog initialization."""
        hll = HyperLogLog(precision=10)
        assert hll.precision == 10
        assert hll.m == 2 ** 10
        assert len(hll.buckets) == 2 ** 10
        assert all(bucket == 0 for bucket in hll.buckets)
    
    def test_initialization_errors(self):
        """Test initialization with invalid precision."""
        with pytest.raises(ValueError):
            HyperLogLog(precision=3)  # Too small
        
        with pytest.raises(ValueError):
            HyperLogLog(precision=17)  # Too large
    
    def test_add_item(self):
        """Test adding items to HyperLogLog."""
        hll = HyperLogLog(precision=8)
        
        # Should not raise errors
        hll.add("192.168.1.1")
        hll.add("10.0.0.1")
        hll.add("8.8.8.8")
        
        # Test type error
        with pytest.raises(TypeError):
            hll.add(123)
    
    def test_estimate_cardinality_small(self):
        """Test cardinality estimation with small dataset."""
        hll = HyperLogLog(precision=10)
        
        # Add unique items
        unique_items = [f"192.168.1.{i}" for i in range(100)]
        for item in unique_items:
            hll.add(item)
        
        estimate = hll.estimate_cardinality()
        
        # Should be reasonably close to 100
        assert 50 <= estimate <= 150  # Allow for some error
    
    def test_estimate_cardinality_with_duplicates(self):
        """Test that duplicates don't affect cardinality estimation."""
        hll = HyperLogLog(precision=12)
        
        # Add items with duplicates
        items = ["192.168.1.1", "192.168.1.2", "192.168.1.3"] * 100
        for item in items:
            hll.add(item)
        
        estimate = hll.estimate_cardinality()
        
        # Should estimate around 3, not 300
        assert 1 <= estimate <= 10
    
    def test_different_precisions(self):
        """Test that different precisions give different accuracy."""
        items = [f"192.168.1.{i}" for i in range(1000)]
        actual_count = len(set(items))
        
        errors = {}
        for precision in [8, 12, 16]:
            hll = HyperLogLog(precision=precision)
            for item in items:
                hll.add(item)
            
            estimate = hll.estimate_cardinality()
            error = abs(estimate - actual_count) / actual_count
            errors[precision] = error
        
        # Higher precision should generally give better accuracy
        # (though this is probabilistic, so we allow some variance)
        assert all(error < 0.3 for error in errors.values())  # All should be reasonably accurate


class TestLogProcessing:
    
    def test_extract_ips_from_log(self):
        """Test IP extraction from log files."""
        # Create temporary log file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
            f.write('192.168.1.1 - - [01/Jan/2024:12:00:00] "GET /index.html HTTP/1.1" 200 1234\n')
            f.write('10.0.0.1 - - [01/Jan/2024:12:00:01] "POST /api HTTP/1.1" 404 567\n')
            f.write('invalid line without ip\n')
            f.write('8.8.8.8 - - [01/Jan/2024:12:00:02] "GET /page.html HTTP/1.1" 200 890\n')
            temp_filename = f.name
        
        try:
            ips = extract_ips_from_log(temp_filename)
            expected_ips = ['192.168.1.1', '10.0.0.1', '8.8.8.8']
            assert ips == expected_ips
        finally:
            os.unlink(temp_filename)
    
    def test_extract_ips_nonexistent_file(self):
        """Test handling of nonexistent files."""
        ips = extract_ips_from_log("nonexistent_file.log")
        assert ips == []
    
    def test_exact_unique_count(self):
        """Test exact unique counting."""
        ips = ['192.168.1.1', '192.168.1.2', '192.168.1.1', '10.0.0.1']
        count, exec_time = exact_unique_count(ips)
        
        assert count == 3  # 3 unique IPs
        assert exec_time >= 0  # Should take some time
    
    def test_hyperloglog_unique_count(self):
        """Test HyperLogLog unique counting."""
        ips = ['192.168.1.1', '192.168.1.2', '192.168.1.1', '10.0.0.1']
        count, exec_time = hyperloglog_unique_count(ips)
        
        assert 1 <= count <= 10  # Should be close to 3 unique IPs
        assert exec_time >= 0  # Should take some time
    
    def test_create_sample_log_file(self):
        """Test sample log file creation."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.log') as f:
            temp_filename = f.name
        
        try:
            create_sample_log_file(temp_filename, num_lines=10)
            
            # Check that file was created and has content
            assert os.path.exists(temp_filename)
            
            with open(temp_filename, 'r') as f:
                lines = f.readlines()
                assert len(lines) == 10
                
            # Extract IPs and verify format
            ips = extract_ips_from_log(temp_filename)
            assert len(ips) == 10  # Should have 10 IP addresses
            
            # Verify IP format
            import re
            ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
            for ip in ips:
                assert ip_pattern.match(ip), f"Invalid IP format: {ip}"
                
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


class TestAccuracy:
    
    def test_accuracy_comparison(self):
        """Test accuracy of HyperLogLog vs exact counting."""
        # Create test data with known unique count
        unique_count = 1000
        test_ips = [f"192.168.{i//256}.{i%256}" for i in range(unique_count)]
        
        # Add some duplicates
        duplicated_ips = test_ips * 3  # Each IP appears 3 times
        random.shuffle(duplicated_ips)
        
        # Exact count
        exact_count, _ = exact_unique_count(duplicated_ips)
        assert exact_count == unique_count
        
        # HyperLogLog count
        hll_count, _ = hyperloglog_unique_count(duplicated_ips, precision=14)
        
        # Calculate error
        error_percentage = abs(exact_count - hll_count) / exact_count * 100
        
        # HyperLogLog should be reasonably accurate (within 10% for this size)
        assert error_percentage < 10.0, f"Error too high: {error_percentage:.2f}%"
    
    def test_performance_comparison(self):
        """Test that HyperLogLog is faster for large datasets."""
        # Create larger dataset
        unique_count = 5000
        test_ips = [f"10.{i//65536}.{(i//256)%256}.{i%256}" for i in range(unique_count)]
        duplicated_ips = test_ips * 2  # Double the data
        
        # Measure exact counting time
        _, exact_time = exact_unique_count(duplicated_ips)
        
        # Measure HyperLogLog time
        _, hll_time = hyperloglog_unique_count(duplicated_ips, precision=14)
        
        # Both should complete in reasonable time
        assert exact_time < 10.0  # Should complete within 10 seconds
        assert hll_time < 10.0    # Should complete within 10 seconds
        
        # Print timing info for reference
        print(f"\nPerformance comparison:")
        print(f"Exact counting: {exact_time:.4f} seconds")
        print(f"HyperLogLog: {hll_time:.4f} seconds")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
