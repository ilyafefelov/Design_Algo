# goit-algo2-hw-01

Домашнє завдання до теми «Аналіз алгоритмів. Стратегія “розділяй і володарюй”»
=====================================================================================

## Завдання 1 (обов’язкове): Пошук максимального та мінімального елементів

Реалізуйте функцію `find_min_max(arr)`, яка знаходить максимальний та мінімальний елементи в списку, використовуючи метод «розділяй і володарюй».

- Функція приймає список чисел довільної довжини.
- Використовується рекурсивний підхід.
- Повертається кортеж у форматі `(мінімум, максимум)`.
- Складність алгоритму: O(n).

## Завдання 2* (опціональне): Пошук k-го найменшого елемента

Реалізуйте алгоритм `quick_select(arr, k)`, який знаходить k-й найменший елемент в несортованому списку, використовуючи принцип Quick Select.

- Функція приймає список чисел та число `k` (індексація починається з 1).
- Використовується вибір опорного елемента (pivot).
- Список не потрібно повністю відсортовувати.
- Очікувана середня складність: O(n).

---

### Приклад використання

```python
from solution import find_min_max, quick_select

arr = [3, 5, 1, 2, 4, 6]
print(find_min_max(arr))    # (1, 6)
print(quick_select(arr, 3)) # 3
```

### Пояснення алгоритмів

#### find_min_max(arr)

1. **Base cases:**  
    - Якщо підмасив містить один елемент, він є і мінімумом, і максимумом.
    - Якщо містить два елементи, порівнюємо їх для визначення мінімуму та максимуму.

2. **Divide:**  
    Розбиваємо масив навпіл, знаходячи середній індекс `mid`.

3. **Conquer:**  
    Рекурсивно отримуємо пари `(minL, maxL)` для лівої частини та `(minR, maxR)` для правої.

4. **Combine:**  
    Повертаємо `(min(minL, minR), max(maxL, maxR))`.

5. **Складність:**  
    Оскільки кожен елемент обробляється лише раз, алгоритм має лінійну складність, O(n).

#### quick_select(arr, k)

1. **Вибір опорного елемента (pivot):**  
    Випадково обираємо елемент і переміщуємо його в кінець підмасиву.

2. **Partition:**  
    Переставляємо елементи так, щоб елементи, менші від pivot, були зліва, а більші — праворуч.

3. **Рекурсія або повернення:**  
    - Якщо позиція `p` pivot дорівнює `k-1`, повертаємо pivot – це й є k-й найменший елемент.
    - Якщо `k-1 < p`, продовжуємо пошук у лівому підмасиві.
    - Якщо `k-1 > p`, шукаємо у правому підмасиві.

4. **Складність:**  
    Середня складність алгоритму — O(n), а в гіршому випадку — O(n²) при невдалому виборі pivot.