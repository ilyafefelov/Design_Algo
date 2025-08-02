# Технічна документація - Домашнє завдання 10

## Загальний огляд

Цей проект демонструє реалізацію та аналіз двох важливих типів алгоритмів:
1. **Рандомізовані алгоритми** (на прикладі QuickSort)
2. **Жадібні алгоритми** (на прикладі задачі покриття множини)

## Завдання 1: Аналіз QuickSort алгоритмів

### Теоретичні основи

**QuickSort** - це алгоритм сортування "розділяй та володарюй" з наступними характеристиками:

- **Середня складність**: O(n log n)
- **Найгірша складність**: O(n²)
- **Просторова складність**: O(log n) для рекурсивних викликів

### Варіанти реалізації

#### 1. Рандомізований QuickSort

```python
def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # Випадковий вибір опорного елемента
    pivot_index = random.randint(0, len(arr) - 1)
    pivot = arr[pivot_index]
    
    # Розділення масиву
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return randomized_quick_sort(left) + middle + randomized_quick_sort(right)
```

**Переваги**:
- Ймовірність найгіршого випадку O(n²) дуже мала
- Очікувана складність завжди O(n log n)
- Надійний на будь-яких даних

**Недоліки**:
- Використання генератора випадкових чисел
- Менш передбачувана поведінка

#### 2. Детермінований QuickSort

```python
def deterministic_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # Фіксований вибір середнього елемента
    pivot_index = len(arr) // 2
    pivot = arr[pivot_index]
    
    # Розділення масиву
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return deterministic_quick_sort(left) + middle + deterministic_quick_sort(right)
```

**Переваги**:
- Передбачувана поведінка
- Не потребує генератора випадкових чисел
- Детермінований результат

**Недоліки**:
- Може деградувати до O(n²) на певних типах даних
- Погана продуктивність на відсортованих масивах

### Методологія тестування

#### Генерація тестових даних
```python
def generate_test_array(size):
    return [random.randint(1, 10000) for _ in range(size)]
```

#### Вимірювання продуктивності
```python
def measure_sorting_time(sort_function, arr):
    arr_copy = copy.deepcopy(arr)
    start_time = time.time()
    sort_function(arr_copy)
    end_time = time.time()
    return end_time - start_time
```

#### Статистичний аналіз
- **Кількість прогонів**: 5 для кожного розміру масиву
- **Метрики**: середній час, дисперсія, мін/макс значення
- **Розміри масивів**: 10K, 50K, 100K, 500K елементів

### Аналіз результатів

Очікувані результати базуються на теоретичному аналізі:

1. **На випадкових даних**: Обидва алгоритми показують схожу продуктивність
2. **На відсортованих даних**: Рандомізований краще за детермінований
3. **Стабільність**: Рандомізований більш стабільний через меншу дисперсію

## Завдання 2: Жадібний алгоритм складання розкладу

### Теоретичні основи

**Задача покриття множини** (Set Cover Problem):
- Дано універсальна множина U (предмети)
- Дано колекція підмножин S (викладачі та їх предмети)
- Знайти мінімальну кількість підмножин, що покривають U

**Жадібна стратегія**:
1. На кожному кроці обирати підмножину, що покриває найбільшу кількість елементів
2. При рівності - використовувати додаткові критерії (вік)

### Структура даних

#### Клас Teacher
```python
class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name           # Ім'я
        self.last_name = last_name             # Прізвище
        self.age = age                         # Вік (критерій вибору)
        self.email = email                     # Контактна інформація
        self.can_teach_subjects = set(can_teach_subjects)  # Можливі предмети
        self.assigned_subjects = set()         # Призначені предмети
```

**Ключові методи**:
- `can_teach(subject)` - перевірка можливості викладання
- `assign_subject(subject)` - призначення предмета
- `get_uncovered_subjects(uncovered)` - отримання перетину з непокритими

### Алгоритм

```python
def create_schedule(subjects, teachers):
    uncovered_subjects = set(subjects)
    available_teachers = teachers.copy()
    selected_teachers = []
    
    while uncovered_subjects and available_teachers:
        best_teacher = None
        max_coverage = 0
        
        # Пошук найкращого викладача
        for teacher in available_teachers:
            teachable_subjects = teacher.get_uncovered_subjects(uncovered_subjects)
            coverage = len(teachable_subjects)
            
            # Критерії вибору:
            # 1. Максимальне покриття
            # 2. Мінімальний вік
            if (coverage > max_coverage or 
                (coverage == max_coverage and coverage > 0 and 
                 (best_teacher is None or teacher.age < best_teacher.age))):
                best_teacher = teacher
                max_coverage = coverage
        
        # Перевірка можливості продовження
        if best_teacher is None or max_coverage == 0:
            break
        
        # Призначення предметів
        subjects_to_assign = best_teacher.get_uncovered_subjects(uncovered_subjects)
        for subject in subjects_to_assign:
            best_teacher.assign_subject(subject)
            uncovered_subjects.remove(subject)
        
        selected_teachers.append(best_teacher)
        available_teachers.remove(best_teacher)
    
    return selected_teachers if not uncovered_subjects else None
```

### Аналіз складності

- **Часова складність**: O(m × n), де m - кількість викладачів, n - кількість предметів
- **Просторова складність**: O(m + n)
- **Апроксимаційне співвідношення**: H(max|Si|), де H - гармонічне число

### Оптимальність

Жадібний алгоритм не гарантує оптимального розв'язку, але:
- Дає гарну апроксимацію для більшості практичних випадків
- Швидкий та простий у реалізації
- Ефективний для задач середнього розміру

## Система тестування

### Структура тестів

1. **Unit тести** для окремих функцій
2. **Integration тести** для повних сценаріїв
3. **Edge case тести** для граничних випадків

### Покриття тестування

#### QuickSort тести:
- Порожні масиви
- Масиви з одним елементом
- Відсортовані масиви
- Масиви з дублікатами
- Від'ємні числа
- Великі масиви

#### Teacher тести:
- Створення об'єктів
- Методи призначення
- Валідація даних

#### Scheduling тести:
- Успішне створення розкладу
- Неможливе покриття
- Оптимальний вибір
- Пріоритет за віком

## Оптимізації та покращення

### Можливі покращення QuickSort:

1. **Гібридний підхід**: Використання Insertion Sort для малих масивів
2. **3-way partitioning**: Оптимізація для масивів з багатьма дублікатами
3. **Медіана-з-трьох**: Кращий вибір pivot елемента
4. **Iterative реалізація**: Уникнення переповнення стеку

### Можливі покращення Scheduling:

1. **Backtracking**: Для знаходження оптимального розв'язку
2. **Динамічне програмування**: Для підзадач
3. **Інші евристики**: Різні критерії вибору викладачів
4. **Паралелізація**: Для великих даних

## Практичне застосування

### QuickSort:
- Сортування в стандартних бібліотеках
- Обробка великих наборів даних
- Real-time системи

### Жадібні алгоритми:
- Планування ресурсів
- Оптимізація розкладів
- Мережеві задачі
- Управління проектами

## Висновки

1. **Рандомізація** підвищує надійність алгоритмів
2. **Жадібні алгоритми** ефективні для багатьох практичних задач
3. **Тестування** критично важливе для валідації алгоритмів
4. **Аналіз складності** допомагає передбачити продуктивність
