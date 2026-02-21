import curses
from generate import MazeGenerator
from rendering import MazeRenderer

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
    
    def __init__(self, stdscr):
        """Initialize the maze application."""
        self.stdscr = stdscr
        self.maze_config = {
            'width': 41,
            'height': 21,
            'entry_position': (1, 0),
            'exit_position': (4, 20)
        }
        
        self.width = self.maze_config['width']
        self.height = self.maze_config['height']
        self.entry = self.maze_config['entry_position']
        self.exit_pos = self.maze_config['exit_position']
        
        self.maze = None
        self.show_solution = False
        self.solution_path = None
        
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
    
    def run(self):
        """Run the interactive maze application."""
        MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                         self.solution_path, self.show_solution)
        
        while True:
            key = self.stdscr.getch()
            
            if key == ord('3'):
                break
            elif key == ord('2'):
                self._solve_maze()
                MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                                 self.solution_path, self.show_solution)
            elif key == ord('1'):
                self._regenerate_maze()
                MazeRenderer.draw(self.stdscr, self.maze, self.entry, self.exit_pos, 
                                 self.solution_path, self.show_solution)


def main(stdscr):
    """Main function to run the application."""
    a_maze_ing = MazeApplication(stdscr)
    a_maze_ing.run()


if __name__ == '__main__':
    curses.wrapper(main)