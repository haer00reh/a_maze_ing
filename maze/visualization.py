import curses


def maze_drawer(stdscr, gen, wall_pair=1):
    stdscr.erase()

    for row in gen.maze:
        for cell in row:
            sy, sx = cell.y * 2, cell.x * 4

            is_path = getattr(cell, 'is_path', False)
            wall_color = curses.color_pair(wall_pair)

            stdscr.addch(sy, sx, curses.ACS_PLUS, wall_color)
            if cell.val & 1:
                for i in range(1, 4):
                    stdscr.addch(sy, sx + i, curses.ACS_HLINE, wall_color)

            if cell.val & 8:
                stdscr.addch(sy + 1, sx, curses.ACS_VLINE, wall_color)

            if cell.val & 2:
                stdscr.addch(sy + 1, sx + 4, curses.ACS_VLINE, wall_color)
            if cell.val & 4:
                for i in range(1, 4):
                    stdscr.addch(sy + 2, sx + i, curses.ACS_HLINE, wall_color)

            stdscr.addch(sy, sx + 4, curses.ACS_PLUS, wall_color)
            stdscr.addch(sy + 2, sx, curses.ACS_PLUS, wall_color)
            stdscr.addch(sy + 2, sx + 4, curses.ACS_PLUS, wall_color)

            if is_path:
                stdscr.addch(
                    sy + 1, sx + 2, curses.ACS_BULLET, curses.color_pair(3)
                    )

            if cell.entry:
                stdscr.addstr(
                    sy + 1, sx + 1, " E ", curses.A_BOLD | wall_color)
            elif cell.exit:
                stdscr.addstr(
                    sy + 1, sx + 1, " X ", curses.A_BOLD | wall_color)
            elif cell.reserved:
                stdscr.addstr(
                    sy + 1, sx + 1, " = ", curses.A_BOLD | wall_color)

    menu_x = (gen.width * 4) + 6
    menu_y_start = 2

    stdscr.addstr(
        menu_y_start, menu_x, "CONTROLS", curses.A_BOLD | curses.A_UNDERLINE)

    options = [
        "1. Color", "2. BFS Generation", "3. DFS Generation", "4. Solver",
        "5. Reset",
        "Q. Quit"
        ]

    for i, opt in enumerate(options):
        target_y = menu_y_start + 2 + i

        max_y, max_x = stdscr.getmaxyx()
        if target_y < max_y and menu_x + len(opt) < max_x:
            try:
                stdscr.addstr(target_y, menu_x, opt)
            except curses.error:
                pass


def run_visualizer(stdscr, gen):
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    current_color = 1
    while True:
        maze_drawer(stdscr, gen, current_color)
        key = stdscr.getch()

        if key == ord('1'):
            current_color = 2 if current_color == 1 else 1
        elif key == ord('2'):
            gen.reset_maze()
            gen.gen_bfs(stdscr, maze_drawer, current_color)
        elif key == ord('3'):
            gen.reset_maze()
            gen.gen_dfs(stdscr, maze_drawer, current_color)
        elif key == ord('4'):
            gen.solve_dfs(stdscr, maze_drawer, current_color)
        elif key == ord('5'):
            gen.reset_maze()
        elif key in [ord('q'), ord('Q')]:
            break
