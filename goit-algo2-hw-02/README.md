# goit-algo2-hw-02

Домашнє завдання до тем «Жадібні алгоритми та динамічне програмування»
=================================================================================

## Завдання 1: Оптимізація черги 3D-принтера в університетській лабораторії

Реалізуйте функцію `optimize_printing(print_jobs, constraints)`, яка:

- Використовує `@dataclass` для структур `PrintJob` та `PrinterConstraints`.
- Групує завдання за пріоритетами (1 — найвищий) жадібно, не перевищуючи:
  - `max_volume` (сума об'ємів у групі)
  - `max_items` (кількість моделей у групі)
- Час друку групи моделей = максимальний `print_time` серед запланованих у групі.
- Повертає словник:
  ```python
  {
    "print_order": ["M1", "M2", ...],  # порядок ID завдань у друці
    "total_time": 360                   # загальний час у хвилинах
  }
  ```

### Приклад
```python
from solution import optimize_printing

print_jobs = [
    {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
    {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
    {"id": "M3", "volume": 120, "priority": 2, "print_time": 150},
]
constraints = {"max_volume": 300, "max_items": 2}
print(optimize_printing(print_jobs, constraints))
# → {'print_order': ['M1','M2','M3'], 'total_time': 270}
```

---
## Завдання 2: Оптимальне розрізання стрижня для максимального прибутку (Rod Cutting)

Реалізуйте два методи динамічного програмування:

1. `rod_cutting_memo(length: int, prices: List[int]) -> Dict`
   - Рекурсія з мемоізацією (`@lru_cache`).
2. `rod_cutting_table(length: int, prices: List[int]) -> Dict`
   - Табуляція (bottom-up).

### Формат повернення для обох методів
```python
{
  "max_profit": int,      # максимальний прибуток
  "cuts": List[int],      # довжини відрізків
  "number_of_cuts": int   # кількість розрізів
}
```

### Приклад
```python
from solution import rod_cutting_memo, rod_cutting_table

length = 5
prices = [2, 5, 7, 8, 10]
print(rod_cutting_memo(length, prices))
# → {'max_profit': 12, 'cuts': [1,2,2], 'number_of_cuts': 2}
print(rod_cutting_table(length, prices))
# → {'max_profit': 12, 'cuts': [2,2,1], 'number_of_cuts': 2}
```

---
## Пояснення алгоритмів

### 1) optimize_printing
1. **Сортування** завдань за полем `priority` (1→3).
2. **Жадібне групування**: додаємо завдання до поточної групи, доки не буде перевищено ліміти `max_volume` або `max_items`.
3. **Фіксація групи**: обчислюємо час як максимальний `print_time` серед моделей у групі, очищуємо групу й продовжуємо.
4. **Результат**: лінійний час O(n).
+**Складність пам'яті**: O(1) додаткової пам'яті (крім вхідних даних).

### 2) rod_cutting_memo
1. Визначаємо рекурсивну формулу:
   profit(r) = max_{1≤i≤r}( prices[i-1] + profit(r-i) )
2. Застосовуємо `@lru_cache` для всіх підзадач довжин ≤ `length`.
3. При відтворенні розрізів фіксуємо вибір `i`, що дає максимум.
+**Складність часу**: O(n^2) внаслідок подвійної рекурсії по довжинах.
+**Складність пам'яті**: O(n) для кешу та глибини рекурсії.

### 3) rod_cutting_table
1. Створюємо масив `dp[0..length]`, ініціалізований нулями.
2. Для кожного `r` (1..length) обчислюємо
   `dp[r] = max_{1≤i≤r}( prices[i-1] + dp[r-i] )`, зберігаючи вибір `i`.
3. Після заповнення отримуємо `dp[length]` і список `cuts`.
+**Складність часу**: O(n^2) через вкладені цикли.
+**Складність пам'яті**: O(n^2) якщо зберігати список `cuts` для кожного підрізу, або O(n) для одного масиву `dp`.
