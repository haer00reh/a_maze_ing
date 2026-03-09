from typing import Any, List


def indexof(arr: List[Any], e: Any) -> int:
    x: int = 0
    for ele in arr:
        if ele == e:
            return x
        x += 1
    return -1


class A:
    def __init__(s, val) -> None:
        s.val = val

    def __eq__(s, ins: object) -> bool:
        if not isinstance(ins, A):
            return NotImplemented
        return s.val == ins.val
