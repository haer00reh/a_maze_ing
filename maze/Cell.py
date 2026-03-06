from typing import List


class Cell:
    def __init__(s, x, y) -> None:
        # s.north_wall = True
        # s.south_wall = True
        # s.east_wall = True
        # s.west_wall = True
        s.is_path: bool = False
        s.entry: bool = False
        s.exit: bool = False
        s.neigbours: List['Cell'] = []
        s.pt: List['Cell'] = []
        s.x: int = x
        s.y: int = y
        s.val: int = 15
        s.reserved: bool = False

    def __str__(s) -> str:
        return f"cell({s.x}, {s.y})"

    def __eq__(s, ins: object) -> bool:
        if not isinstance(ins, Cell):
            return NotImplemented
        return s.x == ins.x and s.y == ins.y

    def before(s, maze) -> 'Cell':
        return maze[s.y][s.x - 1]

    def after(s, maze) -> 'Cell':
        return maze[s.y][s.x + 1]

    def abbove(s, maze) -> 'Cell':
        return maze[s.y - 1][s.x]

    def under(s, maze) -> 'Cell':
        return maze[s.y + 1][s.x]

    def break_north(cell: 'Cell') -> None:
        cell.val -= 1

    def break_est(cell: 'Cell') -> None:
        cell.val -= 2

    def break_south(cell: 'Cell') -> None:
        cell.val -= 4

    def break_west(cell: 'Cell') -> None:
        cell.val -= 8

    # methods to overload [ == ]
