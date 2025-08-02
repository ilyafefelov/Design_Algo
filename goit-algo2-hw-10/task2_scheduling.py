# Визначення класу Teacher
class Teacher:
    """Клас для представлення викладача"""
    
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        """
        Ініціалізація викладача
        
        Args:
            first_name (str): Ім'я викладача
            last_name (str): Прізвище викладача
            age (int): Вік викладача
            email (str): Електронна пошта викладача
            can_teach_subjects (set): Множина предметів, які може викладати
        """
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = set(can_teach_subjects)
        self.assigned_subjects = set()  # Предмети, призначені викладачу
    
    def __str__(self):
        """Строкове представлення викладача"""
        return f"{self.first_name} {self.last_name}, {self.age} років, email: {self.email}"
    
    def __repr__(self):
        """Представлення для debugging"""
        return f"Teacher('{self.first_name}', '{self.last_name}', {self.age}, '{self.email}', {self.can_teach_subjects})"
    
    def can_teach(self, subject):
        """Перевіряє, чи може викладач викладати предмет"""
        return subject in self.can_teach_subjects
    
    def assign_subject(self, subject):
        """Призначає предмет викладачу"""
        if self.can_teach(subject):
            self.assigned_subjects.add(subject)
            return True
        return False
    
    def get_uncovered_subjects(self, uncovered_subjects):
        """Повертає предмети, які викладач може викладати з непокритих"""
        return self.can_teach_subjects.intersection(uncovered_subjects)


def create_schedule(subjects, teachers):
    """
    Створює розклад занять використовуючи жадібний алгоритм
    
    Args:
        subjects (set): Множина всіх предметів
        teachers (list): Список викладачів
    
    Returns:
        list: Список викладачів з призначеними предметами або None, якщо неможливо покрити всі предмети
    """
    # Створюємо копії для роботи
    uncovered_subjects = set(subjects)
    available_teachers = teachers.copy()
    selected_teachers = []
    
    print("Початкові дані:")
    print(f"Предмети для покриття: {sorted(subjects)}")
    print(f"Кількість викладачів: {len(teachers)}")
    print()
    
    # Основний цикл жадібного алгоритму
    step = 1
    while uncovered_subjects and available_teachers:
        print(f"Крок {step}:")
        print(f"Непокриті предмети: {sorted(uncovered_subjects)}")
        
        best_teacher = None
        max_coverage = 0
        
        # Знаходимо найкращого викладача на цьому кроці
        for teacher in available_teachers:
            # Предмети, які цей викладач може покрити з непокритих
            teachable_subjects = teacher.get_uncovered_subjects(uncovered_subjects)
            coverage = len(teachable_subjects)
            
            print(f"  {teacher.first_name} {teacher.last_name}: може покрити {teachable_subjects} ({coverage} предмети)")
            
            # Критерії вибору:
            # 1. Максимальна кількість предметів, які може покрити
            # 2. При рівності - наймолодший вік
            if (coverage > max_coverage or 
                (coverage == max_coverage and coverage > 0 and 
                 (best_teacher is None or teacher.age < best_teacher.age))):
                best_teacher = teacher
                max_coverage = coverage
        
        # Якщо не знайдено викладача, який може покрити хоча б один предмет
        if best_teacher is None or max_coverage == 0:
            print("Не вдалося знайти викладача для покриття залишкових предметів.")
            break
        
        # Призначаємо предмети найкращому викладачу
        subjects_to_assign = best_teacher.get_uncovered_subjects(uncovered_subjects)
        for subject in subjects_to_assign:
            best_teacher.assign_subject(subject)
            uncovered_subjects.remove(subject)
        
        print(f"Обрано: {best_teacher.first_name} {best_teacher.last_name}")
        print(f"Призначені предмети: {sorted(subjects_to_assign)}")
        print(f"Залишилося покрити: {sorted(uncovered_subjects)}")
        print()
        
        # Додаємо викладача до розкладу та видаляємо з доступних
        selected_teachers.append(best_teacher)
        available_teachers.remove(best_teacher)
        
        step += 1
    
    # Перевіряємо, чи всі предмети покриті
    if uncovered_subjects:
        print(f"УВАГА: Неможливо покрити предмети: {sorted(uncovered_subjects)}")
        return None
    
    return selected_teachers


def print_schedule_summary(schedule, subjects):
    """Виводить підсумок розкладу"""
    if not schedule:
        print("Розклад не створено.")
        return
    
    print("=" * 60)
    print("ПІДСУМОК РОЗКЛАДУ")
    print("=" * 60)
    
    total_teachers = len(schedule)
    covered_subjects = set()
    
    for teacher in schedule:
        covered_subjects.update(teacher.assigned_subjects)
    
    print(f"Кількість викладачів у розкладі: {total_teachers}")
    print(f"Покрито предметів: {len(covered_subjects)} з {len(subjects)}")
    print(f"Покриття: {sorted(covered_subjects)}")
    
    if len(covered_subjects) == len(subjects):
        print("✓ Всі предмети успішно покриті!")
    else:
        unpovered = subjects - covered_subjects
        print(f"✗ Не покриті предмети: {sorted(unpovered)}")


def validate_schedule(schedule, subjects):
    """Валідація створеного розкладу"""
    print("\n" + "=" * 60)
    print("ВАЛІДАЦІЯ РОЗКЛАДУ")
    print("=" * 60)
    
    if not schedule:
        print("✗ Розклад не створено")
        return False
    
    all_covered_subjects = set()
    valid = True
    
    for i, teacher in enumerate(schedule, 1):
        print(f"{i}. {teacher}")
        print(f"   Може викладати: {sorted(teacher.can_teach_subjects)}")
        print(f"   Призначено: {sorted(teacher.assigned_subjects)}")
        
        # Перевірка, чи всі призначені предмети дійсно може викладати
        invalid_subjects = teacher.assigned_subjects - teacher.can_teach_subjects
        if invalid_subjects:
            print(f"   ✗ ПОМИЛКА: Призначено предмети, які не може викладати: {sorted(invalid_subjects)}")
            valid = False
        else:
            print(f"   ✓ Всі призначені предмети коректні")
        
        all_covered_subjects.update(teacher.assigned_subjects)
        print()
    
    # Перевірка покриття всіх предметів
    uncovered = subjects - all_covered_subjects
    if uncovered:
        print(f"✗ Не покриті предмети: {sorted(uncovered)}")
        valid = False
    else:
        print("✓ Всі предмети покриті")
    
    # Перевірка на дублювання
    all_assignments = []
    for teacher in schedule:
        all_assignments.extend(teacher.assigned_subjects)
    
    if len(all_assignments) != len(set(all_assignments)):
        print("✗ Виявлено дублювання предметів у розкладі")
        valid = False
    else:
        print("✓ Немає дублювання предметів")
    
    return valid


def analyze_schedule_efficiency(schedule, teachers, subjects):
    """Аналізує ефективність створеного розкладу"""
    print("\n" + "=" * 60)
    print("АНАЛІЗ ЕФЕКТИВНОСТІ")
    print("=" * 60)
    
    if not schedule:
        print("Неможливо проаналізувати - розклад не створено")
        return
    
    used_teachers = len(schedule)
    total_teachers = len(teachers)
    
    print(f"Використано викладачів: {used_teachers} з {total_teachers}")
    print(f"Ефективність використання: {(used_teachers/total_teachers)*100:.1f}%")
    
    # Аналіз завантаження викладачів
    total_assignments = sum(len(teacher.assigned_subjects) for teacher in schedule)
    avg_load = total_assignments / used_teachers if used_teachers > 0 else 0
    
    print(f"Середнє навантаження на викладача: {avg_load:.2f} предмети")
    
    print("\nЗавантаження викладачів:")
    for teacher in schedule:
        load = len(teacher.assigned_subjects)
        utilization = (load / len(teacher.can_teach_subjects)) * 100
        print(f"  {teacher.first_name} {teacher.last_name}: {load} предмети "
              f"({utilization:.1f}% від можливих)")


if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}
    
    # Створення списку викладачів
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
    
    print("ЗАВДАННЯ 2: Складання розкладу занять за допомогою жадібного алгоритму")
    print("=" * 80)
    
    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)
    
    # Виведення розкладу
    if schedule:
        print("РОЗКЛАД ЗАНЯТЬ:")
        print("=" * 40)
        for i, teacher in enumerate(schedule, 1):
            print(f"{i}. {teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(sorted(teacher.assigned_subjects))}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
    
    # Додаткові аналізи
    print_schedule_summary(schedule, subjects)
    validate_schedule(schedule, subjects)
    analyze_schedule_efficiency(schedule, teachers, subjects)
