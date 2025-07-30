"""
Розширена версія MapReduce аналізу з додатковими можливостями
"""

import urllib.request
import urllib.parse
import re
import matplotlib.pyplot as plt
import concurrent.futures
from collections import defaultdict, Counter
import time
import argparse
import json
from typing import List, Dict, Tuple, Optional


class MapReduceWordAnalyzer:
    """
    Клас для аналізу частоти слів з використанням MapReduce
    """
    
    def __init__(self, num_workers: int = 4, min_word_length: int = 3):
        """
        Ініціалізація аналізатора
        
        Args:
            num_workers: Кількість потоків для обробки
            min_word_length: Мінімальна довжина слова для аналізу
        """
        self.num_workers = num_workers
        self.min_word_length = min_word_length
        self.stop_words = {
            'english': {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'a', 'an'},
            'ukrainian': {'і', 'в', 'на', 'з', 'за', 'до', 'від', 'про', 'для', 'як', 'що', 'це', 'той', 'та', 'або', 'але', 'не', 'є', 'був', 'була', 'було', 'були', 'буде', 'будуть', 'мати', 'має', 'мають', 'мав', 'мала', 'мало', 'мали', 'він', 'вона', 'воно', 'вони', 'я', 'ти', 'ми', 'ви', 'мене', 'тебе', 'його', 'її', 'нас', 'вас', 'їх', 'мій', 'твій', 'наш', 'ваш', 'їхній'}
        }
    
    def fetch_text_from_url(self, url: str) -> str:
        """
        Завантажує текст з URL з обробкою помилок
        """
        try:
            # Додаємо User-Agent для уникнення блокування
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                
                # Спробуємо різні кодування
                for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        return content.decode(encoding)
                    except UnicodeDecodeError:
                        continue
                
                # Якщо жодне кодування не спрацювало, використовуємо з ігноруванням помилок
                return content.decode('utf-8', errors='ignore')
                
        except Exception as e:
            print(f"Помилка завантаження з URL {url}: {e}")
            return ""
    
    def clean_and_tokenize(self, text: str, remove_stop_words: bool = True) -> List[str]:
        """
        Очищає текст та розбиває на токени
        """
        # Приводимо до нижнього регістру та витягуємо слова
        words = re.findall(r'\b[a-zA-Zа-яА-ЯёЁіІїЇєЄ]+\b', text.lower())
        
        # Фільтруємо за довжиною
        words = [word for word in words if len(word) >= self.min_word_length]
        
        # Видаляємо стоп-слова якщо потрібно
        if remove_stop_words:
            all_stop_words = set()
            for stop_words in self.stop_words.values():
                all_stop_words.update(stop_words)
            words = [word for word in words if word not in all_stop_words]
        
        return words
    
    def map_function(self, text_chunk: str) -> List[Tuple[str, int]]:
        """Map функція для обробки частини тексту"""
        words = self.clean_and_tokenize(text_chunk)
        return [(word, 1) for word in words]
    
    def reduce_function(self, mapped_results: List[List[Tuple[str, int]]]) -> Dict[str, int]:
        """Reduce функція для агрегації результатів"""
        word_count = defaultdict(int)
        
        for word_list in mapped_results:
            for word, count in word_list:
                word_count[word] += count
        
        return dict(word_count)
    
    def split_text_into_chunks(self, text: str) -> List[str]:
        """Розбиває текст на частини для паралельної обробки"""
        if not text:
            return []
        
        chunk_size = max(len(text) // self.num_workers, 1000)  # Мінімум 1000 символів
        chunks = []
        
        for i in range(self.num_workers):
            start = i * chunk_size
            if i == self.num_workers - 1:
                end = len(text)
            else:
                end = (i + 1) * chunk_size
                # Знаходимо найближчий пробіл
                while end < len(text) and text[end] != ' ':
                    end += 1
            
            if start < len(text):
                chunks.append(text[start:end])
        
        return chunks
    
    def analyze_text(self, text: str) -> Dict[str, int]:
        """
        Виконує повний аналіз тексту з використанням MapReduce
        """
        if not text:
            return {}
        
        print(f"Аналізуємо текст довжиною {len(text)} символів...")
        start_time = time.time()
        
        # Розбиваємо текст на частини
        text_chunks = self.split_text_into_chunks(text)
        print(f"Розбито на {len(text_chunks)} частин")
        
        # Map фаза з багатопотоковістю
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            mapped_results = list(executor.map(self.map_function, text_chunks))
        
        # Reduce фаза
        word_count = self.reduce_function(mapped_results)
        
        end_time = time.time()
        print(f"Аналіз завершено за {end_time - start_time:.2f} секунд")
        print(f"Знайдено {len(word_count)} унікальних слів")
        
        return word_count
    
    def save_results(self, word_count: Dict[str, int], filename: str = "word_analysis.json"):
        """Зберігає результати у файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(word_count, f, ensure_ascii=False, indent=2)
            print(f"Результати збережено у файл {filename}")
        except Exception as e:
            print(f"Помилка збереження: {e}")
    
    def load_results(self, filename: str = "word_analysis.json") -> Optional[Dict[str, int]]:
        """Завантажує результати з файлу"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Помилка завантаження: {e}")
            return None


def visualize_top_words(word_count: Dict[str, int], top_n: int = 10, save_plot: bool = False):
    """
    Розширена візуалізація з можливістю збереження
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
    
    # Створюємо графік з покращеним дизайном
    plt.figure(figsize=(14, 8))
    colors = plt.cm.viridis(range(len(words)))
    bars = plt.bar(range(len(words)), counts, color=colors, edgecolor='black', alpha=0.8)
    
    # Налаштовуємо графік
    plt.title(f'Топ {top_n} найчастіше вживаних слів\n(Загалом проаналізовано {sum(word_count.values())} слів)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Слова', fontsize=12, fontweight='bold')
    plt.ylabel('Частота використання', fontsize=12, fontweight='bold')
    plt.xticks(range(len(words)), words, rotation=45, ha='right', fontsize=10)
    
    # Додаємо значення на стовпці
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.01,
                str(count), ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Покращуємо вигляд
    plt.tight_layout()
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Додаємо статистику
    total_words = sum(word_count.values())
    unique_words = len(word_count)
    coverage = sum(counts) / total_words * 100
    
    stats_text = f'Унікальних слів: {unique_words}\nВсього слів: {total_words}\nПокриття топ-{top_n}: {coverage:.1f}%'
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes, 
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    if save_plot:
        plt.savefig('word_frequency_analysis.png', dpi=300, bbox_inches='tight')
        print("Графік збережено як 'word_frequency_analysis.png'")
    
    plt.show()
    
    # Виводимо детальні результати
    print(f"\nДетальна статистика:")
    print("=" * 50)
    print(f"Загальна кількість слів: {total_words}")
    print(f"Унікальних слів: {unique_words}")
    print(f"Середня частота на слово: {total_words / unique_words:.2f}")
    print(f"\nТоп {top_n} найчастіше вживаних слів:")
    print("-" * 40)
    for i, (word, count) in enumerate(top_words, 1):
        percentage = count / total_words * 100
        print(f"{i:2d}. {word:<20} - {count:>6} разів ({percentage:5.2f}%)")


def main():
    """Головна функція з підтримкою аргументів командного рядка"""
    parser = argparse.ArgumentParser(description='MapReduce Word Frequency Analysis')
    parser.add_argument('--url', type=str, 
                       default='https://www.gutenberg.org/files/74/74-0.txt',
                       help='URL для завантаження тексту')
    parser.add_argument('--workers', type=int, default=4,
                       help='Кількість потоків для обробки')
    parser.add_argument('--top', type=int, default=10,
                       help='Кількість топ слів для відображення')
    parser.add_argument('--min-length', type=int, default=3,
                       help='Мінімальна довжина слова')
    parser.add_argument('--save', action='store_true',
                       help='Зберегти результати та графік')
    
    args = parser.parse_args()
    
    # Створюємо аналізатор
    analyzer = MapReduceWordAnalyzer(
        num_workers=args.workers,
        min_word_length=args.min_length
    )
    
    print("🚀 Запуск MapReduce аналізу частоти слів")
    print("=" * 50)
    print(f"URL: {args.url}")
    print(f"Потоків: {args.workers}")
    print(f"Мінімальна довжина слова: {args.min_length}")
    print(f"Топ слів для відображення: {args.top}")
    print("=" * 50)
    
    # Завантажуємо текст
    print("\n📥 Завантаження тексту...")
    text = analyzer.fetch_text_from_url(args.url)
    
    if not text:
        print("❌ Не вдалося завантажити текст. Використовуємо демонстраційний...")
        text = """
        MapReduce is a programming model and implementation for processing and generating large datasets.
        The MapReduce framework provides a simple interface for implementing distributed computations.
        MapReduce allows programmers to express computations as map and reduce operations.
        The framework automatically handles the parallelization, fault tolerance, and load balancing.
        This makes MapReduce very popular for big data processing in distributed systems.
        Many companies use MapReduce for analyzing large amounts of data efficiently.
        The map function processes input data and produces intermediate key-value pairs.
        The reduce function aggregates the intermediate values associated with the same key.
        Together, map and reduce operations enable powerful data analysis capabilities.
        """
    
    print(f"✅ Завантажено {len(text):,} символів")
    
    # Виконуємо аналіз
    print("\n⚙️ Виконання MapReduce аналізу...")
    word_count = analyzer.analyze_text(text)
    
    if not word_count:
        print("❌ Не вдалося проаналізувати текст")
        return
    
    # Зберігаємо результати якщо потрібно
    if args.save:
        analyzer.save_results(word_count)
    
    # Візуалізуємо результати
    print(f"\n📊 Створення візуалізації топ-{args.top} слів...")
    visualize_top_words(word_count, top_n=args.top, save_plot=args.save)
    
    print("\n✅ Аналіз завершено успішно!")


if __name__ == "__main__":
    main()
