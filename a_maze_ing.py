import curses
from generate import MazeGenerator
from rendering import MazeRenderer
from color_schemes import COLOR_SCHEMES
from resolve_conf import resolve_conf


class MazeSolver:
    """Handles maze solving using backtracking (DFS)."""
    
    @staticmethod
    def solve(maze, start, end):
        """Solve the maze using backtracking (DFS)."""
        height = len(maze)
        width = len(maze[0])
        
        visited = [[False for _ in range(width)] for _ in range(height)]
        stack = [(start[0], start[1], [(start[0], start[1])])]
        visited[start[1]][start[0]] = True
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        while stack:
            x, y, path = stack.pop()
            
            if (x, y) == end:
                return path
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                if (0 <= new_x < width and 
                    0 <= new_y < height and 
                    not visited[new_y][new_x] and 
                    maze[new_y][new_x] in [' ', 'E', 'X']):
                    
                    visited[new_y][new_x] = True
                    stack.append((new_x, new_y, path + [(new_x, new_y)]))
        
        return []


class MazeApplication:
    """Main application for interactive maze solving."""
    
    def __init__(self, stdscr, conf):
        """Initialize the maze application."""
        self.stdscr = stdscr
        self.maze_config = conf
        
        self.width = self.maze_config['width']
        self.height = self.maze_config['height']
        self.entry = self.maze_config['entry']
        self.exit_pos = self.maze_config['exit']
        
        self.maze = None
        self.show_solution = False
        self.solution_path = None
        self.current_color_scheme = 'Cyberpunk'
        
        self._initialize_maze()
        curses.curs_set(0)
    
    def _initialize_maze(self):
        """Initialize a new maze."""
        self.maze = MazeGenerator.generate(self.width, self.height, self.entry, self.exit_pos)
        self.maze[self.entry[1]][self.entry[0]] = 'E'
        self.maze[self.exit_pos[1]][self.exit_pos[0]] = 'X'
    
    def _regenerate_maze(self):
        """Regenerate the maze."""
        self._initialize_maze()
        self.show_solution = False
        self.solution_path = None
    
    def _solve_maze(self):
        """Toggle maze solution display."""
        if not self.show_solution:
            self.solution_path = MazeSolver.solve(self.maze, self.entry, self.exit_pos)
            self.show_solution = True
        else:
            self.show_solution = False
    
    def _select_color_scheme(self):
        """Display color scheme selection menu."""
        schemes = list(COLOR_SCHEMES.keys())
        selected_index = schemes.index(self.current_color_scheme) if self.current_color_scheme in schemes else 0
        
        while True:
            self.stdscr.clear()
            try:
                self.stdscr.addstr(0, 2, 'Select Color Scheme', curses.A_BOLD)
                self.stdscr.addstr(1, 2, '=' * 30)
                
                for idx, scheme in enumerate(schemes):
                    if idx == selected_index:
                        self.stdscr.addstr(3 + idx, 2, f'> {scheme}', curses.A_REVERSE)
                    else:
                        self.stdscr.addstr(3 + idx, 2, f'  {scheme}')
                
                self.stdscr.addstr(3 + len(schemes) + 1, 2, '=' * 30)
                self.stdscr.addstr(3 + len(schemes) + 2, 2, 'Use arrow keys, enter and select, echap to cancel')
            except curses.error:
                pass
            
            self.stdscr.refresh()
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                selected_index = (selected_index - 1) % len(schemes)
            elif key == curses.KEY_DOWN:
                selected_index = (selected_index + 1) % len(schemes)
            elif key in [curses.KEY_ENTER, 10, 13]:
                self.current_color_scheme = schemes[selected_index]
                break
            elif key == 27:
                break
    
    def run(self):
        """Run the interactive maze application."""
        MazeGenerator.carve_42(self.maze, self.width, self.height)
        MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                         self.solution_path, self.show_solution, self.current_color_scheme)
        
        while True:
            key = self.stdscr.getch()
            
            if key == ord('3'):
                break
            elif key == ord('2'):
                self._solve_maze()
                MazeGenerator.carve_42(self.maze, self.width, self.height)
                MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                                 self.solution_path, self.show_solution, self.current_color_scheme)
            elif key == ord('1'):
                self._regenerate_maze()
                MazeGenerator.carve_42(self.maze, self.width, self.height)
                MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                                 self.solution_path, self.show_solution, self.current_color_scheme)
            elif key == ord('4'):
                self._select_color_scheme()
                MazeGenerator.carve_42(self.maze, self.width, self.height)
                MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                                 self.solution_path, self.show_solution, self.current_color_scheme)


def main(stdscr):
    """Main function to run the application."""
    a_maze_ing = MazeApplication(stdscr, resolve_conf())
    a_maze_ing.run()


if __name__ == '__main__':
    res = resolve_conf()
    if len(res) > 0:
        curses.wrapper(main)