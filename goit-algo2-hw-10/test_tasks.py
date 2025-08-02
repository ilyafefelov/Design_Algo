import unittest
import random
import copy
from task1_quicksort import randomized_quick_sort, deterministic_quick_sort, generate_test_array
from task2_scheduling import Teacher, create_schedule


class TestQuickSortAlgorithms(unittest.TestCase):
    """Тести для алгоритмів QuickSort"""
    
    def setUp(self):
        """Підготовка тестових даних"""
        random.seed(42)  # Для відтворюваності результатів
    
    def test_randomized_quick_sort_basic(self):
        """Тест базового функціоналу рандомізованого QuickSort"""
        # Тест на простому масиві
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]
        result = randomized_quick_sort(arr)
        self.assertEqual(result, expected)
    
    def test_deterministic_quick_sort_basic(self):
        """Тест базового функціоналу детермінованого QuickSort"""
        # Тест на простому масиві
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]
        result = deterministic_quick_sort(arr)
        self.assertEqual(result, expected)
    
    def test_empty_array(self):
        """Тест сортування порожнього масиву"""
        arr = []
        self.assertEqual(randomized_quick_sort(arr), [])
        self.assertEqual(deterministic_quick_sort(arr), [])
    
    def test_single_element(self):
        """Тест сортування масиву з одним елементом"""
        arr = [42]
        self.assertEqual(randomized_quick_sort(arr), [42])
        self.assertEqual(deterministic_quick_sort(arr), [42])
    
    def test_already_sorted(self):
        """Тест сортування вже відсортованого масиву"""
        arr = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(randomized_quick_sort(arr), expected)
        self.assertEqual(deterministic_quick_sort(arr), expected)
    
    def test_reverse_sorted(self):
        """Тест сортування масиву, відсортованого в зворотному порядку"""
        arr = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(randomized_quick_sort(arr), expected)
        self.assertEqual(deterministic_quick_sort(arr), expected)
    
    def test_duplicates(self):
        """Тест сортування масиву з дублікатами"""
        arr = [3, 1, 3, 1, 3, 1]
        expected = [1, 1, 1, 3, 3, 3]
        self.assertEqual(randomized_quick_sort(arr), expected)
        self.assertEqual(deterministic_quick_sort(arr), expected)
    
    def test_all_same_elements(self):
        """Тест сортування масиву з однаковими елементами"""
        arr = [5, 5, 5, 5, 5]
        expected = [5, 5, 5, 5, 5]
        self.assertEqual(randomized_quick_sort(arr), expected)
        self.assertEqual(deterministic_quick_sort(arr), expected)
    
    def test_large_array(self):
        """Тест сортування великого масиву"""
        arr = generate_test_array(1000)
        expected = sorted(arr)
        
        self.assertEqual(randomized_quick_sort(arr.copy()), expected)
        self.assertEqual(deterministic_quick_sort(arr.copy()), expected)
    
    def test_negative_numbers(self):
        """Тест сортування масиву з від'ємними числами"""
        arr = [-3, -1, -4, -1, -5, 9, 2, -6]
        expected = [-6, -5, -4, -3, -1, -1, 2, 9]
        self.assertEqual(randomized_quick_sort(arr), expected)
        self.assertEqual(deterministic_quick_sort(arr), expected)
    
    def test_generate_test_array(self):
        """Тест функції генерації тестового масиву"""
        arr = generate_test_array(100)
        self.assertEqual(len(arr), 100)
        self.assertTrue(all(isinstance(x, int) for x in arr))
        self.assertTrue(all(1 <= x <= 10000 for x in arr))


class TestTeacherClass(unittest.TestCase):
    """Тести для класу Teacher"""
    
    def setUp(self):
        """Підготовка тестових даних"""
        self.teacher = Teacher("Іван", "Петров", 35, "ivan@test.com", 
                              {'Математика', 'Фізика'})
    
    def test_teacher_creation(self):
        """Тест створення об'єкта викладача"""
        self.assertEqual(self.teacher.first_name, "Іван")
        self.assertEqual(self.teacher.last_name, "Петров")
        self.assertEqual(self.teacher.age, 35)
        self.assertEqual(self.teacher.email, "ivan@test.com")
        self.assertEqual(self.teacher.can_teach_subjects, {'Математика', 'Фізика'})
        self.assertEqual(self.teacher.assigned_subjects, set())
    
    def test_can_teach(self):
        """Тест методу can_teach"""
        self.assertTrue(self.teacher.can_teach('Математика'))
        self.assertTrue(self.teacher.can_teach('Фізика'))
        self.assertFalse(self.teacher.can_teach('Хімія'))
    
    def test_assign_subject(self):
        """Тест методу assign_subject"""
        # Успішне призначення
        self.assertTrue(self.teacher.assign_subject('Математика'))
        self.assertIn('Математика', self.teacher.assigned_subjects)
        
        # Неуспішне призначення
        self.assertFalse(self.teacher.assign_subject('Хімія'))
        self.assertNotIn('Хімія', self.teacher.assigned_subjects)
    
    def test_get_uncovered_subjects(self):
        """Тест методу get_uncovered_subjects"""
        uncovered = {'Математика', 'Хімія', 'Біологія'}
        result = self.teacher.get_uncovered_subjects(uncovered)
        self.assertEqual(result, {'Математика'})
    
    def test_string_representation(self):
        """Тест строкового представлення викладача"""
        expected = "Іван Петров, 35 років, email: ivan@test.com"
        self.assertEqual(str(self.teacher), expected)


class TestSchedulingAlgorithm(unittest.TestCase):
    """Тести для алгоритму складання розкладу"""
    
    def setUp(self):
        """Підготовка тестових даних"""
        self.subjects = {'Математика', 'Фізика', 'Хімія'}
        self.teachers = [
            Teacher("Іван", "Петров", 35, "ivan@test.com", 
                   {'Математика', 'Фізика'}),
            Teacher("Марія", "Іванова", 30, "maria@test.com", 
                   {'Хімія'}),
            Teacher("Петро", "Сидоров", 40, "petro@test.com", 
                   {'Математика'})
        ]
    
    def test_successful_scheduling(self):
        """Тест успішного створення розкладу"""
        schedule = create_schedule(self.subjects, self.teachers)
        self.assertIsNotNone(schedule)
        
        # Перевірка, що всі предмети покриті
        covered_subjects = set()
        for teacher in schedule:
            covered_subjects.update(teacher.assigned_subjects)
        self.assertEqual(covered_subjects, self.subjects)
    
    def test_impossible_scheduling(self):
        """Тест неможливого створення розкладу"""
        subjects = {'Математика', 'Фізика', 'Хімія', 'Біологія'}
        teachers = [
            Teacher("Іван", "Петров", 35, "ivan@test.com", 
                   {'Математика'})
        ]
        schedule = create_schedule(subjects, teachers)
        self.assertIsNone(schedule)
    
    def test_optimal_selection(self):
        """Тест оптимального вибору викладачів"""
        subjects = {'Математика', 'Фізика'}
        teachers = [
            Teacher("Іван", "Петров", 40, "ivan@test.com", 
                   {'Математика'}),
            Teacher("Марія", "Іванова", 30, "maria@test.com", 
                   {'Математика', 'Фізика'}),  # Кращий вибір - покриває більше
            Teacher("Петро", "Сидоров", 35, "petro@test.com", 
                   {'Фізика'})
        ]
        
        schedule = create_schedule(subjects, teachers)
        self.assertEqual(len(schedule), 1)  # Повинен обрати тільки одного викладача
        self.assertEqual(schedule[0].first_name, "Марія")  # Марія покриває обидва предмети
    
    def test_age_priority(self):
        """Тест пріоритету за віком при однаковому покритті"""
        subjects = {'Математика'}
        teachers = [
            Teacher("Іван", "Петров", 40, "ivan@test.com", 
                   {'Математика'}),
            Teacher("Марія", "Іванова", 30, "maria@test.com", 
                   {'Математика'})  # Молодша, повинна бути обрана
        ]
        
        schedule = create_schedule(subjects, teachers)
        self.assertEqual(len(schedule), 1)
        self.assertEqual(schedule[0].first_name, "Марія")  # Молодша
    
    def test_no_subjects(self):
        """Тест з порожньою множиною предметів"""
        subjects = set()
        schedule = create_schedule(subjects, self.teachers)
        self.assertEqual(schedule, [])  # Повинен повернути порожній список
    
    def test_no_teachers(self):
        """Тест з порожнім списком викладачів"""
        teachers = []
        schedule = create_schedule(self.subjects, teachers)
        self.assertIsNone(schedule)  # Неможливо покрити предмети без викладачів


class TestIntegration(unittest.TestCase):
    """Інтеграційні тести"""
    
    def test_full_scenario(self):
        """Тест повного сценарію з початкового завдання"""
        subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
        teachers = [
            Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", 
                    {'Математика', 'Фізика'}),
            Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", 
                    {'Хімія'}),
            Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", 
                    {'Інформатика', 'Математика'}),
            Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", 
                    {'Біологія', 'Хімія'}),
            Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", 
                    {'Фізика', 'Інформатика'}),
            Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", 
                    {'Біологія'})
        ]
        
        schedule = create_schedule(subjects, teachers)
        self.assertIsNotNone(schedule)
        
        # Перевірка покриття всіх предметів
        covered_subjects = set()
        for teacher in schedule:
            covered_subjects.update(teacher.assigned_subjects)
        self.assertEqual(covered_subjects, subjects)
        
        # Перевірка, що використано мінімальну кількість викладачів
        self.assertLessEqual(len(schedule), len(teachers))
        
        # Перевірка коректності призначень
        for teacher in schedule:
            for subject in teacher.assigned_subjects:
                self.assertIn(subject, teacher.can_teach_subjects)


if __name__ == '__main__':
    # Запуск тестів з детальним виводом
    unittest.main(verbosity=2)
