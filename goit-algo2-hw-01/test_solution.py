import pytest
from solution import find_min_max, quick_select


def test_find_min_max_single():
    assert find_min_max([5]) == (5, 5)


def test_find_min_max_two():
    assert find_min_max([2, 1]) == (1, 2)
    assert find_min_max([1, 3]) == (1, 3)


def test_find_min_max_multiple():
    assert find_min_max([3, 5, 1, 2, 4, 6]) == (1, 6)


def test_find_min_max_negatives():
    assert find_min_max([-10, 0, 10, -20]) == (-20, 10)


@pytest.mark.parametrize("arr,k,expected", [
    ([3, 1, 2], 1, 1),
    ([7, 10, 4, 3, 20, 15], 3, 7),
    ([7, 10, 4, 3, 20, 15], 4, 10),
    ([1, 2, 2, 3], 3, 2),
])
def test_quick_select_valid(arr, k, expected):
    assert quick_select(arr, k) == expected


def test_quick_select_invalid_k():
    with pytest.raises(ValueError):
        quick_select([1, 2, 3], 0)
    with pytest.raises(ValueError):
        quick_select([1, 2, 3], 4)


def test_quick_select_empty():
    with pytest.raises(ValueError):
        quick_select([], 1)


if __name__ == "__main__":
    sample = [3, 5, 1, 2, 4, 6]
    print("Input list:", sample)
    mn, mx = find_min_max(sample)
    print(f"Minimum and Maximum: ({mn}, {mx})")
    k = 3
    kth = quick_select(sample, k)
    print(f"{k}-th smallest element: {kth}")
