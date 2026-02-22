import curses
from color_schemes import COLOR_SCHEMES

class MazeRenderer:
    """Handles rendering of the maze to the terminal."""
    
    _colors_initialized = False
    _color_pairs = {}
    
    @staticmethod
    def _init_colors(color_scheme_name):
        """Initialize color pairs based on the selected color scheme."""
        if not curses.has_colors():
            return
        
        curses.start_color()
        curses.use_default_colors()
        
        scheme = COLOR_SCHEMES.get(color_scheme_name, COLOR_SCHEMES['color 1'])
        pair_num = 1
        
        for key, (fg, bg) in scheme.items():
            curses.init_pair(pair_num, fg, bg)
            MazeRenderer._color_pairs[key] = pair_num
            pair_num += 1
        
        MazeRenderer._colors_initialized = True
    
    @staticmethod
    def draw(stdscr, maze, entry, exit_pos, solution_path=None, show_solution=False, color_scheme='Cyberpunk'):
        """Draw the maze on the screen."""
        MazeRenderer._init_colors(color_scheme)
        stdscr.clear()
        height = len(maze)
        width = len(maze[0])
        
        # all colo pairs
        title_color = curses.color_pair(MazeRenderer._color_pairs.get('title', 0)) if curses.has_colors() else curses.A_BOLD
        wall_color = curses.color_pair(MazeRenderer._color_pairs.get('walls', 0)) if curses.has_colors() else 0
        entry_color = curses.color_pair(MazeRenderer._color_pairs.get('entry', 0)) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        exit_color = curses.color_pair(MazeRenderer._color_pairs.get('exit', 0)) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        solution_color = curses.color_pair(MazeRenderer._color_pairs.get('solution', 0)) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        
        try:
            stdscr.addstr(0, 2, 'A_maze_ing', title_color | curses.A_BOLD)
            stdscr.addstr(1, 2, f'Size: {width}x{height} | Theme: {color_scheme}', curses.A_DIM)
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
                        stdscr.addstr(start_row + y, x * 2, '██', wall_color)
                    elif cell == 'E':
                        stdscr.addstr(start_row + y, x * 2, '✖', entry_color)
                    elif cell == 'X':
                        stdscr.addstr(start_row + y, x * 2, '✖', exit_color)
                    elif is_solution and show_solution:
                            stdscr.addstr(start_row + y, x * 2, '██', solution_color)
                    else:
                        stdscr.addstr(start_row + y, x * 2, '  ')
                except curses.error:
                    pass
        
        try:
            stdscr.addstr(start_row + height + 1, 2, '=== A_maze_ing ===', title_color)
            if show_solution and solution_path:
                stdscr.addstr(start_row + height + 2, 2, '· = lpath')
            stdscr.addstr(start_row + height + 3, 2, "1. Re-generate\n  2. Solve maze\n  3. Quit\n  4. Color scheme")
        except curses.error:
            pass
        
        stdscr.refresh()
