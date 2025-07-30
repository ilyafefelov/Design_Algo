"""
Performance benchmarks for homework 4 tasks.
"""
import time
import random
import string
from task1.solution import Homework
from task2.solution import LongestCommonWord

def generate_random_word(length):
    """Generate a random word of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def benchmark_task1():
    """Benchmark Task 1: Extended Trie functionality."""
    print("=== Task 1 Performance Benchmark ===")
    
    # Create a large dataset
    trie = Homework()
    words = []
    
    # Generate 10,000 words of varying lengths
    print("Generating test data...")
    for i in range(10000):
        word_length = random.randint(3, 15)
        word = generate_random_word(word_length)
        words.append(word)
        trie.put(word, i)
    
    print(f"Created Trie with {len(words)} words")
    
    # Test count_words_with_suffix performance
    print("\nTesting count_words_with_suffix performance...")
    suffixes = ['e', 'ing', 'ed', 'ly', 'tion', 'a', 't']
    
    start_time = time.time()
    for suffix in suffixes:
        count = trie.count_words_with_suffix(suffix)
        print(f"Words ending with '{suffix}': {count}")
    suffix_time = time.time() - start_time
    print(f"Suffix counting took: {suffix_time:.4f} seconds")
    
    # Test has_prefix performance
    print("\nTesting has_prefix performance...")
    prefixes = ['a', 'ab', 'abc', 'te', 'test', 'pre', 'com']
    
    start_time = time.time()
    for prefix in prefixes:
        has_prefix = trie.has_prefix(prefix)
        print(f"Has prefix '{prefix}': {has_prefix}")
    prefix_time = time.time() - start_time
    print(f"Prefix checking took: {prefix_time:.4f} seconds")

def benchmark_task2():
    """Benchmark Task 2: Longest Common Prefix."""
    print("\n=== Task 2 Performance Benchmark ===")
    
    trie = LongestCommonWord()
    
    # Test with different scenarios
    scenarios = [
        {
            'name': 'Small common prefix',
            'strings': ['abcdef', 'abcxyz', 'abcmnp'] * 100  # 300 strings
        },
        {
            'name': 'Long common prefix',
            'strings': ['verylongcommonprefix' + str(i) for i in range(200)]
        },
        {
            'name': 'No common prefix',
            'strings': [generate_random_word(10) for _ in range(150)]
        },
        {
            'name': 'Mixed length strings',
            'strings': ['test' + 'x' * i for i in range(100)]
        }
    ]
    
    for scenario in scenarios:
        print(f"\nTesting scenario: {scenario['name']}")
        print(f"Number of strings: {len(scenario['strings'])}")
        
        start_time = time.time()
        result = trie.find_longest_common_word(scenario['strings'])
        elapsed_time = time.time() - start_time
        
        print(f"Common prefix: '{result[:50]}{'...' if len(result) > 50 else ''}'")
        print(f"Time taken: {elapsed_time:.4f} seconds")

def run_correctness_tests():
    """Run correctness tests to ensure algorithms work properly."""
    print("\n=== Correctness Tests ===")
    
    # Task 1 tests
    print("Task 1 correctness tests:")
    trie1 = Homework()
    test_words = ["apple", "application", "banana", "cat", "car", "card", "care", "careful"]
    for i, word in enumerate(test_words):
        trie1.put(word, i)
    
    # Test required assertions
    assert trie1.count_words_with_suffix("e") == 2, "Failed: words ending with 'e'"
    assert trie1.count_words_with_suffix("ion") == 1, "Failed: words ending with 'ion'"
    assert trie1.count_words_with_suffix("a") == 1, "Failed: words ending with 'a'"
    assert trie1.count_words_with_suffix("at") == 1, "Failed: words ending with 'at'"
    
    assert trie1.has_prefix("app") == True, "Failed: prefix 'app'"
    assert trie1.has_prefix("bat") == False, "Failed: prefix 'bat'"
    assert trie1.has_prefix("ban") == True, "Failed: prefix 'ban'"
    assert trie1.has_prefix("ca") == True, "Failed: prefix 'ca'"
    
    print("✓ Task 1 correctness tests passed")
    
    # Task 2 tests
    print("Task 2 correctness tests:")
    trie2 = LongestCommonWord()
    
    test_cases = [
        (["flower", "flow", "flight"], "fl"),
        (["interspecies", "interstellar", "interstate"], "inters"),
        (["dog", "racecar", "car"], "")
    ]
    
    for strings, expected in test_cases:
        result = trie2.find_longest_common_word(strings)
        assert result == expected, f"Failed: {strings} -> expected '{expected}', got '{result}'"
    
    print("✓ Task 2 correctness tests passed")

if __name__ == "__main__":
    print("Running performance benchmarks for Homework 4")
    print("=" * 50)
    
    # Run correctness tests first
    run_correctness_tests()
    
    # Run performance benchmarks
    benchmark_task1()
    benchmark_task2()
    
    print("\n" + "=" * 50)
    print("Benchmark completed successfully!")
