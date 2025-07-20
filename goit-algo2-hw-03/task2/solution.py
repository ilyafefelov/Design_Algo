import csv
import sys
import timeit
from BTrees.OOBTree import OOBTree


def load_items(csv_path: str) -> list[dict]:
    """
    Завантажує товари з CSV у список словників
    """
    items = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                'ID': row['ID'],
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            })
    return items


def add_item_to_tree(tree: OOBTree, item: dict) -> None:
    price = item['Price']
    if price in tree:
        tree[price].append(item)
    else:
        tree[price] = [item]


def add_item_to_dict(dct: dict, item: dict) -> None:
    price = item['Price']
    if price in dct:
        dct[price].append(item)
    else:
        dct[price] = [item]


def range_query_tree(tree: OOBTree, min_price: float, max_price: float) -> list[dict]:
    result = []
    for price, items in tree.items(min_price, max_price):
        result.extend(items)
    return result


def range_query_dict(dct: dict, min_price: float, max_price: float) -> list[dict]:
    result = []
    for price, items in dct.items():
        if min_price <= price <= max_price:
            result.extend(items)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solution.py <csv_file>")
        sys.exit(1)

    csv_path = sys.argv[1]
    items = load_items(csv_path)

    # Побудова структур
    tree = OOBTree()
    dct = {}
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dct, item)

    # Визначаємо межі запиту (від мін до макс по ціні)
    prices = [item['Price'] for item in items]
    min_price = min(prices)
    max_price = max(prices)

    # Вимірювання часу 100 запитів
    tree_time = timeit.timeit(
        stmt='range_query_tree(tree, min_price, max_price)',
        globals=globals(),
        number=100
    )
    dict_time = timeit.timeit(
        stmt='range_query_dict(dct, min_price, max_price)',
        globals=globals(),
        number=100
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
