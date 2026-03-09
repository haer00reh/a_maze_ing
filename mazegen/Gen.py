from typing import List, Tuple, Dict, Callable
from mazegen.Cell import Cell
import random
import time
from curses import window


class Gen:
    def __init__(s, conf: dict, en: Tuple[int, int], ex: Tuple[int, int],
                 ) -> None:
        """
        inisialize the maze generator values

        :param s: instance
        :param conf: configurations
        :type conf: dict
        :param en: entry point
        :type en: Tuple[int, int]
        :param ex: exit point
        :type ex: Tuple[int, int]
        """
        s.output_file: str = conf['output_file']
        s.width: int = conf['width']
        s.height: int = conf['height']
        s.seed: int = conf['seed']
        s.perfect: bool = conf.get('perfect', True)
        s.maze: List[List[Cell]] = [
            [Cell(x, y) for x in range(s.width)] for y in range(s.height)
            ]
        s.entry: Cell = s.maze[en[1]][en[0]]
        s.exit: Cell = s.maze[ex[1]][ex[0]]
        s.entry.entry = True
        s.exit.exit = True
        s.nib: List[Cell] = []
        s.visited: list[Cell] = []
        s.broken_walls: int = 0
        s.out_path: List[str] = []
        s.solution_path: List[Cell] = []
        s.generated: bool = False
        s.is_solved: bool = False
        s.stored_solution: List[Cell] = []
        for line in s.maze:
            for cell in line:
                s.conf_nighbours(cell)
        s.apply_42_pattern()
        if s.entry.reserved:
            raise ValueError("entry shouldn't belongs to the 42 pattern")
        elif s.exit.reserved:
            raise ValueError("exit shouldn't belongs to the 42 pattern")

    def apply_42_pattern(s) -> None:
        """
        mark cells belongs to 42 pattern

        :param s: instance
        """
        reserved_cells: Dict[int, list[Tuple[int, int]]] = {
            4: [
                (0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (4, 1)
            ],
            2: [
                (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (3, 0),
                (4, 0), (4, 1)
            ]
        }
        start_y = (s.height // 2) - 2
        start_x = (s.width // 2) - 3

        for row in s.maze:
            for cell in row:
                cell.reserved = False

        for dy, dx in reserved_cells[4]:
            target_y, target_x = start_y + dy, start_x + dx
            if 0 <= target_y < s.height and 0 <= target_x < s.width:
                s.maze[target_y][target_x].reserved = True

        for dy, dx in reserved_cells[2]:
            target_y, target_x = start_y + dy, (start_x + 3) + dx
            if 0 <= target_y < s.height and 0 <= target_x < s.width:
                s.maze[target_y][target_x].reserved = True

    def get_rand_choice(s, all: List[Cell]) -> Cell:
        """
        return random choice from list of cells

        :param s: instance
        :param all: list of cells
        :type all: List[Cell]
        :return: random choosen cell
        :rtype: Cell
        """
        return random.choice(all)

    def break_wall(s, main_cell: Cell, target: Cell) -> None:
        """
        break walls between two cells

        :param s: instance
        :param main_cell: first cell
        :type main_cell: Cell
        :param target: seccond cell
        :type target: Cell
        """

        main_cell.pt.append(target)
        s.broken_walls += 1
        if main_cell.y != 0:
            abbove: Cell = main_cell.abbove(s.maze)
            if abbove == target:
                main_cell.break_north()
                target.break_south()
                return
        if main_cell.y != s.height - 1:
            under: Cell = main_cell.under(s.maze)
            if under == target:
                main_cell.break_south()
                target.break_north()
                return
        if main_cell.x != 0:
            before: Cell = main_cell.before(s.maze)
            if before == target:
                main_cell.break_west()
                target.break_est()
                return
        if main_cell.x != s.width - 1:
            after: Cell = main_cell.after(s.maze)
            if after == target:
                main_cell.break_est()
                target.break_west()
                return

    def conf_nighbours(s, c: Cell) -> None:
        """
        configure cell nighbours (add all nighbours)

        :param s: instance
        :param c: cell to configure its nighbours
        :type c: Cell
        """

        if c.x != 0 and c.x < s.width - 1:
            # add s.x - 1 and s.x + 1
            (c.neigbours.append(c.before(s.maze)))
            (c.neigbours.append(c.after(s.maze)))
        elif c.x > 0:
            # add s.x - 1
            (c.neigbours.append(c.before(s.maze)))
        elif c.x < s.width - 1:
            # add s.x + 1
            (c.neigbours.append(c.after(s.maze)))

        if c.y != 0 and c.y < s.height - 1:
            # add c.y - 1 and c.y + 1
            (c.neigbours.append(c.abbove(s.maze)))
            (c.neigbours.append(c.under(s.maze)))
        elif c.y > 0:
            # add c.y - 1
            (c.neigbours.append(c.abbove(s.maze)))
        elif c.y < s.height - 1:
            # add s.y + 1
            (c.neigbours.append(c.under(s.maze)))

    def gen_file(s) -> None:
        """
        generate the outupt file

        :param s: instance
        """

        with open(s.output_file, 'w') as file:
            hex = "0123456789abcdef"
            for line in s.maze:
                for cell in line:
                    file.write(hex[cell.val % 16])
                file.write("\n")
            file.write("\n")
            file.write(f"{s.entry.x},{s.entry.y}\n")
            file.write(f"{s.exit.x},{s.exit.y}\n")
            for char in s.out_path:
                file.write(char)
            file.write("\n")

    def resolve_path(s) -> None:
        """
        get the next movement for the solution path
            (North, South, Est, West)

        :param s: instance
        """

        for i in range(len(s.solution_path) - 1):
            c1 = s.solution_path[i]
            c2 = s.solution_path[i + 1]
            if c2.y < c1.y and s.is_connected(c1, c2):
                s.out_path.append('N')
            if c2.x > c1.x and s.is_connected(c1, c2):
                s.out_path.append('E')
            if c2.y > c1.y and s.is_connected(c1, c2):
                s.out_path.append('S')
            if c2.x < c1.x and s.is_connected(c1, c2):
                s.out_path.append('W')

    def gen_bfs(
            s, stdscr: window, drawer: Callable,
            color: str
            ) -> None:
        """
        generate maze using breath first search algorithm

        :param s: instance
        :param stdscr: standard output (where to print)
        :type stdscr: window
        :param drawer: drawer fun (dep injection)
        :type drawer: Callable
        :param color: color to be drawn with
        :type color: Dict[str, Tuple[int, int]]
        """
        random.seed(s.seed)
        s.visited.append(s.entry)
        queue: List[Cell] = [s.entry]
        while queue:
            ele = queue.pop(random.randint(0, len(queue) - 1))
            nighbours = s.get_valid_neighbours(ele)
            random.shuffle(nighbours)
            for nib in nighbours:
                if nib not in s.visited:
                    s.visited.append(nib)
                    s.break_wall(ele, nib)
                    queue.append(nib)

                    drawer(stdscr, s, color)
                    stdscr.refresh()
                    time.sleep(0.03)

        # make imperfect if configured
        if not s.perfect:
            s.make_imperfect()
            drawer(stdscr, s, color)
            stdscr.refresh()
        s.generated = True
        s.stored_solution = []
        s.solution_path = []

    def gen_dfs(
            s, stdscr: window, drawer: Callable,
            color: str
            ) -> None:
        """
        generate maze using deep first search algorithm

        :param s: instance
        :param stdscr: standard output (where to print)
        :type stdscr: window
        :param drawer: drawer fun (dep injection)
        :type drawer: Callable
        :param color: color to be drawn with
        :type color: Dict[str, Tuple[int, int]]
        """
        random.seed(s.seed)
        s.visited.append(s.entry)
        stack: List[Cell] = [s.entry]
        while s.broken_walls < (s.width * s.height) - 1:
            if (len(stack) == 0):
                break
            nighbours = [
                n for n in s.get_valid_neighbours(stack[-1])
                if n not in s.visited
                ]
            if len(nighbours) == 0:
                stack.pop()
            else:
                ele = stack[-1]
                target: Cell = random.choice(nighbours)
                s.visited.append(target)
                s.break_wall(ele, target)
                stack.append(target)

                drawer(stdscr, s, color)
                stdscr.refresh()
                time.sleep(0.03)

        if not s.perfect:
            s.make_imperfect()
            drawer(stdscr, s, color)
            stdscr.refresh()
        s.generated = True
        s.stored_solution = []
        s.solution_path = []

    def solve_dfs(
            s, stdscr: window, drawer: Callable,
            color: str
            ) -> None:
        """
        maze solver

        :param s: instance
        :param stdscr: standard output (where to print)
        :param drawer: drawer fun (dep injection)
        :param color: color to be drawn with
        """

        s.visited = [s.entry]
        stack: List[Cell] = [s.entry]
        s.entry.is_path = True
        if (not s.generated):
            return

        if (s.is_solved):
            for e in s.solution_path:
                e.is_path = False
            s.is_solved = False
            s.stored_solution = s.solution_path
            drawer(stdscr, s, color)
            stdscr.refresh()
            time.sleep(0.03)
            return

        if (len(s.stored_solution) > 0):
            for cell in s.stored_solution:
                cell.is_path = True
                drawer(stdscr, s, color)
                stdscr.refresh()
                time.sleep(0.03)
                s.is_solved = True
            return

        while stack:
            cur: Cell = stack[-1]
            if cur == s.exit:
                break
            cur_paths = [c for c in s.get_valid_neighbours(cur)
                         if c not in s.visited and s.is_connected(cur, c)
                         ]
            if len(cur_paths) > 0:
                target: Cell = random.choice(cur_paths)
                s.visited.append(target)
                stack.append(target)
                target.is_path = True
                drawer(stdscr, s, color)
                stdscr.refresh()
                time.sleep(0.03)
            else:
                bad_path = stack.pop()
                bad_path.is_path = False
                drawer(stdscr, s, color)
                stdscr.refresh()
                time.sleep(0.03)
        s.solution_path = stack
        s.resolve_path()
        s.gen_file()
        s.is_solved = True

    def get_valid_neighbours(s, cell: Cell) -> List[Cell]:
        """
        check for not visited and not connected cells nighbours
            and return them

        :param s: instance
        :param cell: target cell
        :type cell: Cell
        :return: valid neighbours
        :rtype: List[Cell]
        """
        return [
            cell for cell in cell.neigbours
            if cell not in s.visited
            and not cell.reserved
            ]

    def reset_maze(s) -> None:
        """
        reseting the maze to be all closed

        :param s: instance
        """
        for line in s.maze:
            for cell in line:
                cell.val = 15
                cell.is_path = False
        s.visited = []
        s.broken_walls = 0
        s.generated = False
        s.is_solved = False
        s.out_path = []

    def reset_solver(s) -> None:
        """
        Docstring for reset_solver

        :param s: Description
        """
        for line in s.maze:
            for cell in line:
                cell.is_path = False

    def is_connected(self, c1: Cell, c2: Cell):
        """
        check if two cells are connected

        :param self: instance
        :param c1: cell
        :type c1: Cell
        :param c2: cell
        : type c2: cell
        """
        if c2.y < c1.y:
            return not (c1.val & 1)
        if c2.x > c1.x:
            return not (c1.val & 2)
        if c2.y > c1.y:
            return not (c1.val & 4)
        if c2.x < c1.x:
            return not (c1.val & 8)
        return False

    def make_imperfect(s, removal_percentage: float = 0.1) -> None:
        """
            removes random walls to create loops (imperfect maze).
            removal_percentage: percentage of removable walls (default 10%)

        :param s: instance
        :param removal_percentage: how many walls should be breaked (%)
        :type removal_percentage: float
        """
        random.seed(s.seed)
        potential_removals = []
        for row in s.maze:
            for cell in row:
                if cell.reserved:
                    continue
                for neighbor in cell.neigbours:
                    if neighbor.reserved:
                        continue
                    if neighbor.y < cell.y and (cell.val & 1):
                        potential_removals.append((cell, neighbor, 'north'))
                    elif neighbor.x > cell.x and (cell.val & 2):
                        potential_removals.append((cell, neighbor, 'east'))
        walls_to_remove = max(
            1, int(len(potential_removals) * removal_percentage))

        if potential_removals:
            walls_selected = random.sample(
                potential_removals, min(
                    walls_to_remove, len(potential_removals)))

            for cell, neighbor, direction in walls_selected:
                s.break_wall(cell, neighbor)
