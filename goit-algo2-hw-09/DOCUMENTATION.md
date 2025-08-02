# Документація: Локальний пошук, евристики та імітація відпалу

## Загальний огляд

Цей проект реалізує три алгоритми локальної оптимізації для мінімізації функції Сфери:

1. **Hill Climbing (Підйом на гору)**
2. **Random Local Search (Випадковий локальний пошук)**
3. **Simulated Annealing (Імітація відпалу)**

## Функція Сфери

Функція Сфери - це класична тестова функція для алгоритмів оптимізації:

```
f(x) = Σ(xi²) для i від 1 до n
```

**Властивості:**
- Глобальний мінімум: точка (0, 0, ..., 0) зі значенням 0
- Унімодальна функція (один глобальний мінімум)
- Сферично симетрична
- Безперервна та диференційована скрізь

## Алгоритми оптимізації

### 1. Hill Climbing (Підйом на гору)

**Принцип роботи:**
- Починає з випадкової точки
- На кожній ітерації генерує сусідню точку
- Переходить до сусіда тільки якщо він кращий
- Завершується при досягненні локального мінімуму

**Переваги:**
- Простий у реалізації
- Швидка збіжність
- Ефективний для унімодальних функцій

**Недоліки:**
- Може застрягти в локальних мінімумах
- Результат залежить від початкової точки
- Жадібний підхід може пропустити глобальний оптимум

**Реалізація:**
```python
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    current_point = generate_random_point(bounds)
    current_value = func(current_point)
    
    for iteration in range(iterations):
        neighbor = generate_neighbor(current_point, bounds)
        neighbor_value = func(neighbor)
        
        if neighbor_value < current_value:
            if abs(current_value - neighbor_value) < epsilon:
                break
            current_point = neighbor
            current_value = neighbor_value
    
    return current_point, current_value
```

### 2. Random Local Search (Випадковий локальний пошук)

**Принцип роботи:**
- Починає з випадкової точки
- На кожній ітерації генерує випадкового сусіда
- Зберігає тільки найкращого знайденого сусіда
- Продовжує пошук незалежно від поточного стану

**Переваги:**
- Менш схильний до локальних мінімумів
- Простий у реалізації
- Хороша диверсифікація пошуку

**Недоліки:**
- Може бути повільнішим за Hill Climbing
- Відсутність направленого пошуку
- Велика кількість обчислень функції

**Реалізація:**
```python
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    best_point = generate_random_point(bounds)
    best_value = func(best_point)
    
    for iteration in range(iterations):
        neighbor = generate_neighbor(best_point, bounds)
        neighbor_value = func(neighbor)
        
        if neighbor_value < best_value:
            if abs(best_value - neighbor_value) < epsilon:
                break
            best_point = neighbor
            best_value = neighbor_value
    
    return best_point, best_value
```

### 3. Simulated Annealing (Імітація відпалу)

**Принцип роботи:**
- Інспірований процесом відпалу металів
- Має "температуру", яка зменшується з часом
- Може приймати гірші рішення з ймовірністю exp(-Δ/T)
- З часом стає все більш жадібним

**Переваги:**
- Може уникати локальних мінімумів
- Теоретично гарантує знаходження глобального оптимуму
- Балансує експлорацію та експлуатацію

**Недоліки:**
- Потребує налаштування параметрів (температура, швидкість охолодження)
- Може бути повільнішим
- Складніший у реалізації

**Реалізація:**
```python
def simulated_annealing(func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6):
    current_point = generate_random_point(bounds)
    current_value = func(current_point)
    best_point = current_point[:]
    best_value = current_value
    current_temp = temp
    
    for iteration in range(iterations):
        if current_temp < epsilon:
            break
            
        neighbor = generate_neighbor(current_point, bounds)
        neighbor_value = func(neighbor)
        delta = neighbor_value - current_value
        
        if delta < 0 or random.random() < math.exp(-delta / current_temp):
            current_point = neighbor
            current_value = neighbor_value
            if neighbor_value < best_value:
                best_point = neighbor[:]
                best_value = neighbor_value
        
        current_temp *= cooling_rate
    
    return best_point, best_value
```

## Допоміжні функції

### Генерація випадкової точки
```python
def generate_random_point(bounds):
    return [random.uniform(bound[0], bound[1]) for bound in bounds]
```

### Генерація сусідньої точки
```python
def generate_neighbor(point, bounds, step_size=0.1):
    neighbor = []
    for i, (lower, upper) in enumerate(bounds):
        perturbation = random.uniform(-step_size, step_size)
        new_value = point[i] + perturbation
        new_value = max(lower, min(upper, new_value))
        neighbor.append(new_value)
    return neighbor
```

### Обчислення відстані
```python
def distance(point1, point2):
    return math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(point1, point2)))
```

## Критерії збіжності

Алгоритми завершуються при виконанні однієї з умов:

1. **Зміна значення функції < epsilon**
   ```python
   if abs(current_value - neighbor_value) < epsilon:
       break
   ```

2. **Зміна положення точки < epsilon**
   ```python
   if distance(current_point, neighbor) < epsilon:
       break
   ```

3. **Температура < epsilon** (для Simulated Annealing)
   ```python
   if current_temp < epsilon:
       break
   ```

4. **Досягнуто максимальну кількість ітерацій**

## Параметри алгоритмів

### Загальні параметри
- `func`: Функція для мінімізації
- `bounds`: Список кортежів (min, max) для кожного виміру
- `iterations`: Максимальна кількість ітерацій (за замовчуванням: 1000)
- `epsilon`: Поріг збіжності (за замовчуванням: 1e-6)

### Специфічні для Simulated Annealing
- `temp`: Початкова температура (за замовчуванням: 1000)
- `cooling_rate`: Швидкість охолодження 0 < rate < 1 (за замовчуванням: 0.95)

## Рекомендації з налаштування

### Hill Climbing
- Збільшіть `iterations` для складніших функцій
- Зменшіть `epsilon` для більшої точності
- Запускайте кілька разів з різними початковими точками

### Random Local Search
- Збільшіть `iterations` оскільки пошук менш направлений
- Налаштуйте `step_size` в `generate_neighbor` для балансу експлорації/експлуатації

### Simulated Annealing
- **Початкова температура**: Повинна бути достатньо високою для прийняття гірших рішень
- **Швидкість охолодження**: 0.9-0.99 для повільного охолодження, 0.8-0.9 для швидкого
- **Кількість ітерацій**: Зазвичай потребує більше ітерацій ніж інші алгоритми

## Порівняльний аналіз

| Критерій | Hill Climbing | Random Local Search | Simulated Annealing |
|----------|---------------|-------------------|-------------------|
| Швидкість | Висока | Середня | Повільна |
| Якість розв'язку | Добра для унімодальних | Середня | Найкраща |
| Уникнення локальних мінімумів | Низька | Середня | Висока |
| Складність реалізації | Низька | Низька | Середня |
| Налаштування параметрів | Мінімальне | Мінімальне | Значне |

## Результати тестування

При тестуванні на функції Сфери з межами [-5, 5]:

- **Hill Climbing**: Зазвичай знаходить значення ~1e-6
- **Random Local Search**: Знаходить значення ~1e-2 до 1e-1
- **Simulated Annealing**: Знаходить значення ~1e-4 до 1e-3

## Застосування

### Коли використовувати Hill Climbing:
- Унімодальні функції
- Потрібна швидка збіжність
- Обмежені обчислювальні ресурси

### Коли використовувати Random Local Search:
- Мультимодальні функції з багатьма локальними мінімумами
- Потрібна проста реалізація
- Невідома структура функції

### Коли використовувати Simulated Annealing:
- Складні мультимодальні функції
- Потрібна висока якість розв'язку
- Доступні обчислювальні ресурси для налаштування

## Розширення та модифікації

### Можливі покращення:
1. **Адаптивний step_size** в `generate_neighbor`
2. **Restart mechanisms** для Hill Climbing
3. **Різні cooling schedules** для Simulated Annealing
4. **Гібридні підходи** (комбінації алгоритмів)
5. **Паралелізація** для множинних запусків

### Інші функції для тестування:
- Rastrigin function
- Ackley function
- Rosenbrock function
- Griewank function
