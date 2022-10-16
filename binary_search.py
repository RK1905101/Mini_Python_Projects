# binary_search.py
from typing import Union


def binary_search(array: list, target: Union[int, str, float]) -> str:
    lower_bound: int = 0
    upper_bound: int = len(array) - 1

    while lower_bound <= upper_bound:
        mid = (lower_bound + upper_bound) // 2
        if array[mid] < target:
            lower_bound = mid + 1
        elif array[mid] > target:
            upper_bound = mid - 1
        elif array[mid] == target:
            return f"The position of {target} found in {mid},"
    else:
        return None
