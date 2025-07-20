from typing import List, Dict
from dataclasses import dataclass
import random
from functools import lru_cache

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Returns:
        Dict з полями "print_order" та "total_time"
    """
    # Підготувати дані
    jobs = [PrintJob(**job) for job in print_jobs]
    cons = PrinterConstraints(**constraints)
    # Сортуємо за пріоритетом (1 найвищий)
    jobs.sort(key=lambda x: x.priority)

    print_order: List[str] = []
    total_time = 0
    current_group: List[PrintJob] = []
    current_volume = 0.0

    def flush_group():
        nonlocal total_time, print_order, current_group
        if not current_group:
            return
        # Час групи = максимальний час друку серед завдань у групі
        group_time = max(job.print_time for job in current_group)
        total_time += group_time
        print_order.extend(job.id for job in current_group)
        current_group.clear()

    for job in jobs:
        # Спроба додати в поточну групу
        if (len(current_group) < cons.max_items and
            current_volume + job.volume <= cons.max_volume):
            current_group.append(job)
            current_volume += job.volume
        else:
            # Фіксація поточної групи
            flush_group()
            # Започаткувати нову
            current_group.append(job)
            current_volume = job.volume

    # Фіксація останньої групи
    flush_group()

    return {"print_order": print_order, "total_time": total_time}


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальне розрізання стрижня через мемоізацію

    Returns:
        Dict з полями "max_profit", "cuts", "number_of_cuts"
    """
    @lru_cache(None)
    def best(r: int):
        if r == 0:
            return 0, []
        max_profit = 0
        best_cuts: List[int] = []
        for i in range(1, r + 1):
            profit_rest, cuts_rest = best(r - i)
            current = prices[i - 1] + profit_rest
            if current > max_profit:
                max_profit = current
                best_cuts = cuts_rest + [i]
        return max_profit, best_cuts

    profit, cuts = best(length)
    return {
        "max_profit": profit,
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1)
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальне розрізання стрижня через табуляцію

    Returns:
        Dict з полями "max_profit", "cuts", "number_of_cuts"
    """
    dp = [0] * (length + 1)
    cut_choice: List[List[int]] = [[] for _ in range(length + 1)]

    for r in range(1, length + 1):
        max_profit = 0
        best_cuts: List[int] = []
        for i in range(1, r + 1):
            current = prices[i - 1] + dp[r - i]
            if current > max_profit:
                max_profit = current
                best_cuts = cut_choice[r - i] + [i]
        dp[r] = max_profit
        cut_choice[r] = best_cuts

    cuts = cut_choice[length]
    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": max(0, len(cuts) - 1)
    }


if __name__ == "__main__":
    # Демонстрація
    print("=== Printing Optimization ===")
    jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 2, "print_time": 150},
    ]
    constraints = {"max_volume": 300, "max_items": 2}
    print(optimize_printing(jobs, constraints))

    print("\n=== Rod Cutting (Memo) ===")
    length = 5
    prices = [2, 5, 7, 8, 10]
    print(rod_cutting_memo(length, prices))

    print("\n=== Rod Cutting (Table) ===")
    print(rod_cutting_table(length, prices))
