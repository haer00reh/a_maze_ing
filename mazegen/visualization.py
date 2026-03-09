import curses
from mazegen.color_schemes import COLOR_SCHEMES
from curses import window
from mazegen import Gen


def maze_drawer(
        stdscr: window, gen: Gen, scheme_name='color 1') -> None:
    """
    drawer func to drawe the maze

    :param stdscr: standard output
    :type stdscr: window
    :param gen: maze gen instance
    :type gen: Gen
    :param scheme_name: option of the choosen color
    """

    stdscr.erase()
    max_y, max_x = stdscr.getmaxyx()

    for row in gen.maze:
        for cell in row:
            sy, sx = cell.y * 2, cell.x * 4

            is_path = getattr(cell, 'is_path', False)
            wall_color = curses.color_pair(1) | curses.A_BOLD
            entry_color = curses.color_pair(2) | curses.A_BOLD
            exit_color = curses.color_pair(3) | curses.A_BOLD
            solution_color = curses.color_pair(4)

            gy, gx = cell.y, cell.x
            if gy == 0 and gx == 0:
                char = '┏'
            elif gy == 0 and gx > 0:
                char = '┳'
            elif gx == 0 and gy > 0:
                char = '┣'
            else:
                char = '╋'
            try:
                stdscr.addch(sy, sx, char, wall_color)
            except curses.error:
                pass

            if cell.val & 1:
                for i in range(1, 4):
                    try:
                        stdscr.addch(sy, sx + i, '━', wall_color)
                    except curses.error:
                        pass

            if cell.val & 8:
                try:
                    stdscr.addch(sy + 1, sx, '┃', wall_color)
                except curses.error:
                    pass

            if cell.val & 2:
                try:
                    stdscr.addch(sy + 1, sx + 4, '┃', wall_color)
                except curses.error:
                    pass
            if cell.val & 4:
                for i in range(1, 4):
                    try:
                        stdscr.addch(sy + 2, sx + i, '━', wall_color)
                    except curses.error:
                        pass

            gy, gx = cell.y, cell.x + 1
            if gy == 0 and gx == gen.width:
                char = '┓'
            elif gy == 0 and gx < gen.width:
                char = '┳'
            elif gx == gen.width and gy > 0:
                char = '┫'
            else:
                char = '╋'
            try:
                stdscr.addch(sy, sx + 4, char, wall_color)
            except curses.error:
                pass

            gy, gx = cell.y + 1, cell.x
            if gy == gen.height and gx == 0:
                char = '┗'
            elif gy == gen.height and gx > 0:
                char = '┻'
            elif gx == 0 and gy < gen.height:
                char = '┣'
            else:
                char = '╋'
            try:
                stdscr.addch(sy + 2, sx, char, wall_color)
            except curses.error:
                pass

            gy, gx = cell.y + 1, cell.x + 1
            if gy == gen.height and gx == gen.width:
                char = '┛'
            elif gy == gen.height and gx < gen.width:
                char = '┻'
            elif gx == gen.width and gy < gen.height:
                char = '┫'
            else:
                char = '╋'
            try:
                stdscr.addch(sy + 2, sx + 4, char, wall_color)
            except curses.error:
                pass

            if is_path:
                path_north = False
                path_south = False
                path_east = False
                path_west = False

                for neighbor in cell.neigbours:
                    if getattr(neighbor, 'is_path', False):
                        if neighbor.y < cell.y and not (cell.val & 1):
                            path_north = True
                        elif neighbor.x > cell.x and not (cell.val & 2):
                            path_east = True
                        elif neighbor.y > cell.y and not (cell.val & 4):
                            path_south = True
                        elif neighbor.x < cell.x and not (cell.val & 8):
                            path_west = True

                if (path_north and path_south and
                        not path_east and not path_west):
                    char = '┃'
                elif (path_east and path_west
                        and not path_north and not path_south):
                    char = '━'
                elif path_north and path_east:
                    char = '┗'
                elif path_north and path_west:
                    char = '┛'
                elif path_south and path_east:
                    char = '┏'
                elif path_south and path_west:
                    char = '┓'
                else:
                    char = '•'

                try:
                    stdscr.addch(sy + 1, sx + 2, char, solution_color)
                except curses.error:
                    pass

            if cell.entry:
                try:
                    stdscr.addstr(sy + 1, sx + 1, " E ", entry_color)
                except curses.error:
                    pass
            elif cell.exit:
                try:
                    stdscr.addstr(sy + 1, sx + 1, " X ", exit_color)
                except curses.error:
                    pass
            elif cell.reserved:
                try:
                    stdscr.addstr(sy + 1, sx + 1, "███", wall_color)
                except curses.error:
                    pass

    maze_bottom = (gen.height * 2) + 3
    menu_y = maze_bottom + 1

    title_color = curses.color_pair(5) | curses.A_BOLD

    controls_text = (f"[1-8] Color: {scheme_name}  \n[B] BFS  \n[D] DFS  "
                     f"\n[S] Solve  \n[R] Reset  \n[Q] Quit")
    menu_x = 2

    if menu_y < max_y:
        try:
            stdscr.addstr(menu_y, menu_x, controls_text, title_color)
        except curses.error:
            pass


def run_visualizer(stdscr: window, gen: Gen) -> None:
    """
    function responsable for visualize the maze with the menu

    :param stdscr: standard output
    :param gen: maze gen instance
    """
    curses.start_color()
    curses.curs_set(0)

    scheme_names = list(COLOR_SCHEMES.keys())
    current_scheme_idx = 0

    def init_color_scheme(scheme_name):
        scheme = COLOR_SCHEMES[scheme_name]
        curses.init_pair(1, *scheme['walls'])
        curses.init_pair(2, *scheme['entry'])
        curses.init_pair(3, *scheme['exit'])
        curses.init_pair(4, *scheme['solution'])
        curses.init_pair(5, *scheme['title'])

    init_color_scheme(scheme_names[current_scheme_idx])

    while True:
        maze_drawer(stdscr, gen, scheme_names[current_scheme_idx])
        key = stdscr.getch()

        if key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'),
                   ord('6'), ord('7'), ord('8')]:
            idx = key - ord('1')
            if 0 <= idx < len(scheme_names):
                current_scheme_idx = idx
                init_color_scheme(scheme_names[current_scheme_idx])
        elif key in [ord('b')]:
            gen.reset_maze()
            gen.gen_bfs(stdscr, maze_drawer, scheme_names[current_scheme_idx])
        elif key in [ord('d')]:
            gen.reset_maze()
            gen.gen_dfs(stdscr, maze_drawer, scheme_names[current_scheme_idx])
        elif key in [ord('s')]:
            gen.reset_solver()
            gen.solve_dfs(
                stdscr, maze_drawer, scheme_names[current_scheme_idx])
        elif key in [ord('r')]:
            gen.reset_maze()
        elif key in [ord('q')]:
            break
