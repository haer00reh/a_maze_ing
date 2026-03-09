from typing import Any, List


def indexof(arr: List[Any], e: Any) -> int:
    x: int = 0
    for ele in arr:
        if ele == e:
            return x
        x += 1
    return -1
