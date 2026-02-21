import curses

class MazeRenderer:
    """Handles rendering of the maze to the terminal."""
    
    @staticmethod
    def draw(stdscr, maze, entry, exit_pos, solution_path=None, show_solution=False):
        """Draw the maze on the screen."""
        stdscr.clear()
        height = len(maze)
        width = len(maze[0])
        
        try:
            stdscr.addstr(0, 2, 'A_maze_ing', curses.A_BOLD)
            stdscr.addstr(1, 2, f'Size: {width}x{height}', curses.A_DIM)
            if show_solution and solution_path:
                stdscr.addstr(2, 2, f'Solution: {len(solution_path)} steps', curses.A_DIM)
        except curses.error:
            pass
        
        start_row = 4
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                try:
                    is_solution = solution_path and (x, y) in solution_path
                    
                    if cell == '#':
                        stdscr.addstr(start_row + y, x * 2, '██')
                    elif cell == 'E':
                        stdscr.addstr(start_row + y, x * 2, '✖', curses.A_BOLD)
                    elif cell == 'X':
                        stdscr.addstr(start_row + y, x * 2, '✖', curses.A_BOLD)
                    elif is_solution and show_solution:
                        if x % 2 == 1 and y % 2 == 1:
                            stdscr.addstr(start_row + y, x * 2, '▪', curses.A_BOLD)
                        else:
                            stdscr.addstr(start_row + y, x * 2, '▫', curses.A_BOLD)
                    else:
                        stdscr.addstr(start_row + y, x * 2, '  ')
                except curses.error:
                    pass
        
        try:
            stdscr.addstr(start_row + height + 1, 2, '=== A_maze_ing ===')
            if show_solution and solution_path:
                stdscr.addstr(start_row + height + 2, 2, '· = lpath')
            stdscr.addstr(start_row + height + 3, 2, "1. Re-generate\n  2. Solve maze\n  3. quit")
        except curses.error:
            pass
        
        stdscr.refresh()
