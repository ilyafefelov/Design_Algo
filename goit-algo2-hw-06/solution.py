"""
MapReduce Word Frequency Analysis with Visualization
Task 6: Analyze word frequency from URL text using MapReduce paradigm
"""

import urllib.request
import re
import matplotlib.pyplot as plt
import concurrent.futures
from collections import defaultdict, Counter
from functools import reduce
import threading


def fetch_text_from_url(url):
    """
    Завантажує текст з URL-адреси
    
    Args:
        url (str): URL для завантаження тексту
        
    Returns:
        str: Текст з URL
    """
    try:
        with urllib.request.urlopen(url) as response:
            # Декодуємо з різними кодуваннями
            content = response.read()
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text = content.decode('latin-1')
                except UnicodeDecodeError:
                    text = content.decode('cp1252', errors='ignore')
            return text
    except Exception as e:
        print(f"Помилка завантаження з URL: {e}")
        return ""


def map_function(text_chunk):
    """
    Map функція для MapReduce - обробляє частину тексту та повертає слова
    
    Args:
        text_chunk (str): Частина тексту для обробки
        
    Returns:
        list: Список кортежів (слово, 1)
    """
    # Очищуємо текст від пунктуації та приводимо до нижнього регістру
    words = re.findall(r'\b[a-zA-Zа-яА-ЯёЁіІїЇєЄ]+\b', text_chunk.lower())
    
    # Фільтруємо короткі слова (менше 3 символів)
    words = [word for word in words if len(word) >= 3]
    
    return [(word, 1) for word in words]


def reduce_function(mapped_results):
    """
    Reduce функція для MapReduce - агрегує результати підрахунку слів
    
    Args:
        mapped_results (list): Результати map функції
        
    Returns:
        dict: Словник з частотою слів
    """
    word_count = defaultdict(int)
    
    for word_list in mapped_results:
        for word, count in word_list:
            word_count[word] += count
    
    return dict(word_count)


def split_text_into_chunks(text, num_chunks=4):
    """
    Розбиває текст на частини для паралельної обробки
    
    Args:
        text (str): Вихідний текст
        num_chunks (int): Кількість частин
        
    Returns:
        list: Список частин тексту
    """
    if not text:
        return []
    
    chunk_size = len(text) // num_chunks
    chunks = []
    start = 0
    
    for i in range(num_chunks):
        if i == num_chunks - 1:
            # Остання частина включає весь залишок
            end = len(text)
        else:
            end = start + chunk_size
            # Знаходимо найближчий пробіл, щоб не розрізати слова
            while end < len(text) and text[end] != ' ':
                end += 1
        
        chunks.append(text[start:end])
        start = end
        
        # Пропускаємо пробіли на початку наступної частини
        while start < len(text) and text[start] == ' ':
            start += 1
    
    return chunks


def mapreduce_word_count(text, num_workers=4):
    """
    Реалізація MapReduce для підрахунку частоти слів з багатопотоковістю
    
    Args:
        text (str): Текст для аналізу
        num_workers (int): Кількість потоків
        
    Returns:
        dict: Словник з частотою слів
    """
    # Розбиваємо текст на частини
    text_chunks = split_text_into_chunks(text, num_workers)
    
    # Map фаза з багатопотоковістю
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        mapped_results = list(executor.map(map_function, text_chunks))
    
    # Reduce фаза
    word_count = reduce_function(mapped_results)
    
    return word_count


def visualize_top_words(word_count, top_n=10):
    """
    Візуалізує топ слова за частотою використання
    
    Args:
        word_count (dict): Словник з частотою слів
        top_n (int): Кількість топ слів для відображення
    """
    if not word_count:
        print("Немає даних для візуалізації")
        return
    
    # Отримуємо топ слова
    top_words = Counter(word_count).most_common(top_n)
    
    if not top_words:
        print("Не знайдено слів для візуалізації")
        return
    
    words, counts = zip(*top_words)
    
    # Створюємо графік
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(words)), counts, color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Налаштовуємо графік
    plt.title(f'Топ {top_n} найчастіше вживаних слів', fontsize=16, fontweight='bold')
    plt.xlabel('Слова', fontsize=12)
    plt.ylabel('Частота', fontsize=12)
    plt.xticks(range(len(words)), words, rotation=45, ha='right')
    
    # Додаємо значення на стовпці
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3)
    plt.show()
    
    # Виводимо результати у консоль
    print(f"\nТоп {top_n} найчастіше вживаних слів:")
    print("-" * 40)
    for i, (word, count) in enumerate(top_words, 1):
        print(f"{i:2d}. {word:<15} - {count:>4} разів")


def main():
    """
    Головна функція програми
    """
    # URL для завантаження тексту (приклад - "Гутенберг проект")
    url = "https://www.gutenberg.org/files/74/74-0.txt"  # Adventures of Tom Sawyer
    
    print("Завантаження тексту з URL...")
    text = fetch_text_from_url(url)
    
    if not text:
        print("Не вдалося завантажити текст з URL")
        # Використовуємо приклад тексту для демонстрації
        text = """
        This is a sample text for demonstrating the MapReduce word frequency analysis.
        The text contains various words that will be counted and analyzed.
        Some words appear multiple times in this text to show the frequency analysis.
        MapReduce is a programming paradigm for processing large datasets.
        This implementation uses multithreading to process text chunks in parallel.
        The visualization will show the most frequent words in the text.
        """
        print("Використовуємо демонстраційний текст...")
    
    print(f"Завантажено {len(text)} символів")
    
    # Застосовуємо MapReduce для аналізу частоти слів
    print("Виконуємо аналіз частоти слів за допомогою MapReduce...")
    word_count = mapreduce_word_count(text, num_workers=4)
    
    print(f"Знайдено {len(word_count)} унікальних слів")
    
    # Візуалізуємо результати
    print("Створюємо візуалізацію...")
    visualize_top_words(word_count, top_n=10)


if __name__ == "__main__":
    main()
