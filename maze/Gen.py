from typing import List, Tuple, Dict
from maze.Cell import Cell
import random
import time


class Gen:
    def __init__(s, conf: dict, en: Tuple[int, int], ex: Tuple[int, int],
                 ) -> None:
        s.width: int = conf['width']
        s.height: int = conf['height']
        s.seed: int = conf['seed']
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
        for line in s.maze:
            for cell in line:
                s.conf_nighbours(cell)
        s.apply_42_pattern()
        if s.entry.reserved:
            raise ValueError("entry shouldn't belongs to the 42 pattern")
        elif s.exit.reserved:
            raise ValueError("exit shouldn't belongs to the 42 pattern")

    def apply_42_pattern(s) -> None:
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
        return random.choice(all)

    def break_wall(s, main_cell: Cell, target: Cell) -> None:
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

    def gen_bfs(s, stdscr, drawer, color) -> None:
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
                    time.sleep(0.1)

    def gen_dfs(s, stdscr, drawer, color) -> None:
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
                time.sleep(0.1)

    def solve_dfs(s, stdscr, drawer, color) -> None:

        s.visited = [s.entry]
        stack: List[Cell] = [s.entry]
        s.entry.is_path = True

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
                time.sleep(0.1)
            else:
                bad_path = stack.pop()
                bad_path.is_path = False
                drawer(stdscr, s, color)
                stdscr.refresh()
                time.sleep(0.1)

    def get_valid_neighbours(s, cell: Cell) -> List[Cell]:
        return [
            cell for cell in cell.neigbours
            if cell not in s.visited
            and not cell.reserved
            ]

    def reset_maze(s) -> None:
        for line in s.maze:
            for cell in line:
                cell.val = 15
                cell.is_path = False
        s.visited = []
        s.broken_walls = 0

    def is_connected(self, c1, c2):
        if c2.y < c1.y:
            return not (c1.val & 1)
        if c2.x > c1.x:
            return not (c1.val & 2)
        if c2.y > c1.y:
            return not (c1.val & 4)
        if c2.x < c1.x:
            return not (c1.val & 8)
        return False
