from typing import List


class Cell:
    def __init__(s, x: int, y: int) -> None:
        """
        initalize the cell object

        :param s: instance
        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int
        """
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
        """
        to print the maze

        :param s: instance
        :return: string of cells with its coordinates
        :rtype: str
        """
        return f"cell({s.x}, {s.y})"

    def __eq__(s, ins: object) -> bool:
        """
        comparison between two cells

        :param s: instance
        :param ins: another instance
        :type ins: object
        :return: if two instances are equal
        :rtype: bool
        """
        if not isinstance(ins, Cell):
            return NotImplemented
        return s.x == ins.x and s.y == ins.y

    def before(s, maze: List[List['Cell']]) -> 'Cell':
        """
        return cell before the self cell

        :param s: Description
        :param maze: the maze
        :type maze: List[List['Cell']]
        :return: cell before main cell
        :rtype: Cell
        """
        return maze[s.y][s.x - 1]

    def after(s, maze: List[List['Cell']]) -> 'Cell':
        """
        return cell after the self cell

        :param s: Description
        :param maze: the maze
        :type maze: List[List['Cell']]
        :return: cell after main cell
        :rtype: Cell
        """
        return maze[s.y][s.x + 1]

    def abbove(s, maze: List[List['Cell']]) -> 'Cell':
        """
        return cell abbove the self cell

        :param s: Description
        :param maze: the maze
        :type maze: List[List['Cell']]
        :return: cell abbove main cell
        :rtype: Cell
        """
        return maze[s.y - 1][s.x]

    def under(s, maze: List[List['Cell']]) -> 'Cell':
        """
        return cell under the self cell

        :param s: Description
        :param maze: the maze
        :type maze: List[List['Cell']]
        :return: cell under main cell
        :rtype: Cell
        """
        return maze[s.y + 1][s.x]

    def break_north(cell) -> None:
        """
        break north wall

        :param cell: cell
        """
        cell.val -= 1

    def break_est(cell) -> None:
        """
        break est wall

        :param cell: cell
        """
        cell.val -= 2

    def break_south(cell) -> None:
        """
        break south wall

        :param cell: cell
        """
        cell.val -= 4

    def break_west(cell) -> None:
        """
        break west wall

        :param cell: cell
        """
        cell.val -= 8
