"""
Тести для перевірки функціональності MapReduce аналізу частоти слів
"""

import unittest
from unittest.mock import patch, MagicMock
from solution import (
    map_function, 
    reduce_function, 
    split_text_into_chunks,
    mapreduce_word_count,
    fetch_text_from_url
)


class TestMapReduceWordCount(unittest.TestCase):
    """Тести для MapReduce функціональності"""
    
    def setUp(self):
        """Підготовка тестових даних"""
        self.sample_text = "This is a test text. This text is for testing the MapReduce functionality."
        self.expected_words = ["this", "text", "test", "for", "testing", "the", "mapreduce", "functionality"]
    
    def test_map_function(self):
        """Тест map функції"""
        result = map_function("This is a test text")
        expected = [("this", 1), ("test", 1), ("text", 1)]
        self.assertEqual(result, expected)
    
    def test_map_function_filters_short_words(self):
        """Тест фільтрації коротких слів у map функції"""
        result = map_function("I am a big cat")
        expected = [("big", 1), ("cat", 1)]
        self.assertEqual(result, expected)
    
    def test_map_function_removes_punctuation(self):
        """Тест видалення пунктуації у map функції"""
        result = map_function("Hello, world! How are you?")
        expected = [("hello", 1), ("world", 1), ("how", 1), ("are", 1), ("you", 1)]
        self.assertEqual(result, expected)
    
    def test_reduce_function(self):
        """Тест reduce функції"""
        mapped_results = [
            [("word", 1), ("test", 1)],
            [("word", 1), ("example", 1)],
            [("test", 1), ("word", 1)]
        ]
        result = reduce_function(mapped_results)
        expected = {"word": 3, "test": 2, "example": 1}
        self.assertEqual(result, expected)
    
    def test_split_text_into_chunks(self):
        """Тест розбиття тексту на частини"""
        text = "This is a long text that should be split into multiple chunks for processing"
        chunks = split_text_into_chunks(text, 3)
        
        # Перевіряємо, що повернуто правильну кількість частин
        self.assertEqual(len(chunks), 3)
        
        # Перевіряємо, що частини не порожні
        for chunk in chunks:
            self.assertTrue(len(chunk) > 0)
        
        # Перевіряємо, що всі слова присутні (можуть бути пробіли втрачені на межах)
        original_words = set(text.split())
        combined_words = set()
        for chunk in chunks:
            combined_words.update(chunk.split())
        
        self.assertEqual(original_words, combined_words)
    
    def test_split_text_empty(self):
        """Тест розбиття порожнього тексту"""
        result = split_text_into_chunks("", 4)
        self.assertEqual(result, [])
    
    def test_mapreduce_word_count_integration(self):
        """Інтеграційний тест MapReduce"""
        text = "test word test another word test"
        result = mapreduce_word_count(text, num_workers=2)
        
        expected = {"test": 3, "word": 2, "another": 1}
        self.assertEqual(result, expected)
    
    def test_mapreduce_empty_text(self):
        """Тест MapReduce з порожнім текстом"""
        result = mapreduce_word_count("", num_workers=2)
        self.assertEqual(result, {})
    
    def test_mapreduce_single_worker(self):
        """Тест MapReduce з одним потоком"""
        text = "single worker test single"
        result = mapreduce_word_count(text, num_workers=1)
        
        expected = {"single": 2, "worker": 1, "test": 1}
        self.assertEqual(result, expected)


class TestURLFetching(unittest.TestCase):
    """Тести для завантаження з URL"""
    
    @patch('urllib.request.urlopen')
    def test_fetch_text_success_utf8(self, mock_urlopen):
        """Тест успішного завантаження UTF-8 тексту"""
        mock_response = MagicMock()
        mock_response.read.return_value = b"Test content in UTF-8"
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = fetch_text_from_url("http://example.com")
        self.assertEqual(result, "Test content in UTF-8")
    
    @patch('urllib.request.urlopen')
    def test_fetch_text_encoding_fallback(self, mock_urlopen):
        """Тест обробки різних кодувань"""
        # Імітуємо контент, який не може бути декодований як UTF-8
        mock_response = MagicMock()
        mock_response.read.return_value = b"\x80\x81\x82"  # Недійсний UTF-8
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = fetch_text_from_url("http://example.com")
        # Результат не повинен бути порожнім (використається резервне кодування)
        self.assertTrue(len(result) > 0)
    
    @patch('urllib.request.urlopen')
    def test_fetch_text_network_error(self, mock_urlopen):
        """Тест обробки мережевої помилки"""
        mock_urlopen.side_effect = Exception("Network error")
        
        result = fetch_text_from_url("http://example.com")
        self.assertEqual(result, "")


class TestWordProcessing(unittest.TestCase):
    """Тести для обробки слів"""
    
    def test_case_insensitive_processing(self):
        """Тест обробки різних регістрів"""
        text = "Word word WORD Word"
        result = mapreduce_word_count(text, num_workers=1)
        self.assertEqual(result, {"word": 4})
    
    def test_unicode_text_processing(self):
        """Тест обробки українського тексту"""
        text = "слово тест слово українська мова"
        result = mapreduce_word_count(text, num_workers=1)
        expected = {"слово": 2, "тест": 1, "українська": 1, "мова": 1}
        self.assertEqual(result, expected)
    
    def test_mixed_language_processing(self):
        """Тест обробки змішаного тексту"""
        text = "English word українське слово English слово"
        result = mapreduce_word_count(text, num_workers=1)
        expected = {"english": 2, "word": 1, "українське": 1, "слово": 2}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Запуск тестів
    unittest.main(verbosity=2)
