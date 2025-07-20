import os
import sys

# Ensure the current file’s directory is on sys.path so "solution.py" can be imported
sys.path.insert(0, os.path.dirname(__file__))



import pytest
from solution import optimize_printing, rod_cutting_memo, rod_cutting_table

# Test data for optimize_printing
@pytest.fixture
def printing_constraints():
    return {"max_volume": 300, "max_items": 2}

@pytest.fixture
def jobs_same_priority():
    return [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

@pytest.fixture
def jobs_diff_priority():
    return [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
    ]

@pytest.fixture
def jobs_overflow():
    return [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]


def test_printing_same_priority(jobs_same_priority, printing_constraints):
    res = optimize_printing(jobs_same_priority, printing_constraints)
    assert res["print_order"] == ["M1", "M2", "M3"]
    assert res["total_time"] == 270


def test_printing_diff_priority(jobs_diff_priority, printing_constraints):
    res = optimize_printing(jobs_diff_priority, printing_constraints)
    assert res["print_order"] == ["M2", "M1", "M3"]
    assert res["total_time"] == 270


def test_printing_overflow(jobs_overflow, printing_constraints):
    res = optimize_printing(jobs_overflow, printing_constraints)
    assert res["print_order"] == ["M1", "M2", "M3"]
    assert res["total_time"] == 450

# Test data for rod cutting
@pytest.mark.parametrize("length,prices,expected_profit,expected_cuts", [
    (5, [2, 5, 7, 8, 10], 12, [2, 2, 1]),
    (3, [1, 3, 8], 8, [3]),
    (4, [3, 5, 6, 7], 12, [1, 1, 1, 1]),
])
def test_rod_cutting_methods(length, prices, expected_profit, expected_cuts):
    # Test memoized version
    memo_res = rod_cutting_memo(length, prices)
    assert memo_res["max_profit"] == expected_profit
    assert memo_res["cuts"] == expected_cuts
    assert memo_res["number_of_cuts"] == max(0, len(expected_cuts) - 1)

    # Test tabulation version
    table_res = rod_cutting_table(length, prices)
    assert table_res["max_profit"] == expected_profit
    assert table_res["cuts"] == expected_cuts
    assert table_res["number_of_cuts"] == max(0, len(expected_cuts) - 1)

if __name__ == "__main__":
    pytest.main(["-q"])
