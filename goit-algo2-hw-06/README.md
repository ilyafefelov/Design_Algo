# GoIT Algo2 HW-06: MapReduce Word Frequency Analysis

## Опис завдання

Цей проект реалізує аналіз частоти слів у тексті з використанням парадигми MapReduce та візуалізацію результатів.

## Функціональність

1. **Завантаження тексту з URL** - програма завантажує текст з заданої URL-адреси
2. **MapReduce аналіз** - використовує парадигму MapReduce для підрахунку частоти слів
3. **Багатопотоковість** - ефективно використовує багатопотоковість для обробки тексту
4. **Візуалізація** - створює графік топ-слів за частотою використання

## Структура проекту

```
goit-algo2-hw-06/
├── solution.py          # Основний файл з реалізацією
├── test_solution.py     # Тести для перевірки функціональності
├── requirements.txt     # Залежності проекту
└── README.md           # Документація
```

## Основні компоненти

### MapReduce Implementation

- **Map функція**: Обробляє частини тексту та повертає пари (слово, 1)
- **Reduce функція**: Агрегує результати та підраховує загальну частоту слів
- **Багатопотоковість**: Використовує ThreadPoolExecutor для паралельної обробки

### Особливості реалізації

1. **Очищення тексту**: Видаляє пунктуацію та приводить до нижнього регістру
2. **Фільтрація**: Відфільтровує слова менше 3 символів
3. **Розбиття тексту**: Розбиває текст на частини без розрізання слів
4. **Підтримка кодувань**: Обробляє різні кодування тексту (UTF-8, Latin-1, CP1252)

### Візуалізація

- Створює стовпчастий графік топ слів
- Відображає частоту використання кожного слова
- Підтримує налаштування кількості слів для відображення

## Запуск

```bash
python solution.py
```

## Приклад використання

```python
from solution import mapreduce_word_count, visualize_top_words, fetch_text_from_url

# Завантаження тексту
url = "https://www.gutenberg.org/files/74/74-0.txt"
text = fetch_text_from_url(url)

# Аналіз частоти слів
word_count = mapreduce_word_count(text, num_workers=4)

# Візуалізація
visualize_top_words(word_count, top_n=10)
```

## Критерії прийняття

✅ Код успішно завантажує текст із заданої URL-адреси  
✅ Код коректно виконує аналіз частоти слів із використанням MapReduce  
✅ Візуалізація відображає топ-слова за частотою використання  
✅ Код ефективно використовує багатопотоковість  
✅ Код читабельний та відповідає стандартам PEP 8  

## Технології

- Python 3.x
- matplotlib для візуалізації
- concurrent.futures для багатопотоковості
- urllib для завантаження з URL
- re для обробки тексту

## Автор

Виконано в рамках курсу GoIT Algorithms and Data Structures
