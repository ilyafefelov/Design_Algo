# Домашнє завдання 8: Алгоритми контролю потоку та обмеження швидкості

## Опис завдання

Реалізація механізмів обмеження частоти повідомлень у чат-системі для запобігання спаму двома способами:

1. **Sliding Window Rate Limiter** - точний контроль часових інтервалів
2. **Throttling Rate Limiter** - фіксований інтервал між повідомленнями

## Завдання 1: Sliding Window Rate Limiter

Алгоритм відстежує кількість повідомлень у заданому часовому вікні (10 секунд) та обмежує користувачів, якщо ліміт (1 повідомлення) перевищено.

### Функціональність:
- `_cleanup_window()` - очищення застарілих запитів
- `can_send_message()` - перевірка можливості відправлення
- `record_message()` - запис нового повідомлення
- `time_until_next_allowed()` - розрахунок часу очікування

## Завдання 2: Throttling Rate Limiter

Алгоритм забезпечує фіксований інтервал очікування (10 секунд) між повідомленнями користувача.

### Функціональність:
- `can_send_message()` - перевірка на основі часу останнього повідомлення
- `record_message()` - запис з оновленням часу
- `time_until_next_allowed()` - розрахунок часу до наступного дозволеного

## Файли:
- `task1.py` - Sliding Window Rate Limiter
- `task2.py` - Throttling Rate Limiter
- `test_task1.py` - тести для завдання 1
- `test_task2.py` - тести для завдання 2
- `main.py` - запуск обох завдань
- `requirements.txt` - залежності (якщо потрібні)
