import random


def find_min_max(arr):
    """
    Finds the minimum and maximum elements in a list using divide and conquer.
    :param arr: list of numbers
    :return: tuple (min, max)
    """
    if not isinstance(arr, list) or len(arr) == 0:
        raise ValueError("List must be non-empty")

    def helper(left, right):
        # Base case: one element
        if left == right:
            return arr[left], arr[left]
        # Base case: two elements
        if right == left + 1:
            if arr[left] < arr[right]:
                return arr[left], arr[right]
            else:
                return arr[right], arr[left]
        # Divide
        mid = (left + right) // 2
        minL, maxL = helper(left, mid)
        minR, maxR = helper(mid + 1, right)
        # Combine results
        return (min(minL, minR), max(maxL, maxR))

    return helper(0, len(arr) - 1)


def quick_select(arr, k):
    """
    Finds the k-th smallest element in an unsorted list using Quick Select.
    :param arr: list of numbers
    :param k: 1-based index for the k-th smallest element
    :return: the k-th smallest element
    """
    if not isinstance(arr, list) or len(arr) == 0:
        raise ValueError("List must be non-empty")
    n = len(arr)
    if not isinstance(k, int) or k < 1 or k > n:
        raise ValueError("k must be between 1 and the length of the list")

    # work on a copy to avoid mutating original
    a = arr.copy()
    target = k - 1

    def partition(left, right):
        pivot_idx = random.randint(left, right)
        pivot = a[pivot_idx]
        # move pivot to end
        a[pivot_idx], a[right] = a[right], a[pivot_idx]
        store = left
        for i in range(left, right):
            if a[i] < pivot:
                a[i], a[store] = a[store], a[i]
                store += 1
        # move pivot to its final place
        a[store], a[right] = a[right], a[store]
        return store

    def select(left, right):
        if left == right:
            return a[left]
        pivot_index = partition(left, right)
        if pivot_index == target:
            return a[pivot_index]
        elif target < pivot_index:
            return select(left, pivot_index - 1)
        else:
            return select(pivot_index + 1, right)

    return select(0, n - 1)


if __name__ == "__main__":
    # Sample demonstration of functionality 
    sample = [3, 5, 1, 2, 4, 6]
    print("Input array:", sample)
    minimum, maximum = find_min_max(sample)
    print(f"Minimum element: {minimum}")
    print(f"Maximum element: {maximum}")
    k = 3
    kth_value = quick_select(sample, k)
    print(f"{k}-th smallest element: {kth_value}")
