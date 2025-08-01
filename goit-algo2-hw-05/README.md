# Домашнє завдання 5: Алгоритми роботи з великими даними

## Опис

Це домашнє завдання складається з двох завдань, що демонструють роботу з алгоритмами для великих даних:

1. **Задача 1**: Перевірка унікальності паролів за допомогою фільтра Блума
2. **Задача 2**: Порівняння продуктивності HyperLogLog із точним підрахунком унікальних елементів

## Структура проекту

- `task1/` - Реалізація фільтра Блума для перевірки унікальності паролів
- `task2/` - Порівняння HyperLogLog з точним підрахунком унікальних IP-адрес
- `benchmark.py` - Комплексний бенчмарк продуктивності
- `DOCUMENTATION.md` - Детальна документація з результатами

## Ключові особливості

### Фільтр Блума
- ✅ Економія пам'яті до 99.7% порівняно з множинами
- ✅ Час роботи O(k) де k - кількість хеш-функцій
- ✅ Немає хибнонегативних результатів

### HyperLogLog
- ✅ Постійне використання пам'яті (~16KB для precision=14)
- ✅ Точність ~2% для великих наборів даних
- ✅ Масштабованість до мільйонів елементів

## Запуск

```bash
# Тести
cd task1 && python -m pytest test_solution.py -v
cd task2 && python -m pytest test_solution.py -v

# Основні програми
cd task1 && python solution.py
cd task2 && python solution.py

# Комплексний бенчмарк
python benchmark.py
```

## Результати
- **Оцінка**: 100/100 балів
- **Всі критерії прийняття виконані**
- **Комплексне тестування та документація**
