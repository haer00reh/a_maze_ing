import curses
import random

def generate_maze(width, height):
    random.seed()
    
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    cells_x = (width - 1) // 2
    cells_y = (height - 1) // 2
    
    if cells_x < 1 or cells_y < 1:
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                maze[y][x] = ' '
        return maze
    
    start_x, start_y = 1, 1
    maze[start_y][start_x] = ' '
    stack = [(start_x, start_y)]
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    
    while stack:
        current_x, current_y = stack[-1]
        neighbors = []
        
        for dx, dy in directions:
            new_x, new_y = current_x + dx, current_y + dy
            if 1 <= new_x < width - 1 and 1 <= new_y < height - 1:
                if maze[new_y][new_x] == '#':
                    neighbors.append((new_x, new_y, dx, dy))
        
        if neighbors:
            new_x, new_y, dx, dy = random.choice(neighbors)
            wall_x = current_x + dx // 2
            wall_y = current_y + dy // 2
            maze[wall_y][wall_x] = ' '
            maze[new_y][new_x] = ' '
            stack.append((new_x, new_y))
        else:
            stack.pop()
    
    if width % 2 == 0:
        for y in range(1, height - 1):
            if maze[y][width - 3] == ' ':
                maze[y][width - 2] = ' '
    
    if height % 2 == 0:
        for x in range(1, width - 1):
            if maze[height - 3][x] == ' ':
                maze[height - 2][x] = ' '
    
    return maze

def solve_maze(maze, start, end):
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

def draw_maze(stdscr, maze, entry, exit_pos, solution_path=None, show_solution=False):
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
                    stdscr.addstr(start_row + y, x * 2, '▓▓')
                elif cell == 'E':
                    stdscr.addstr(start_row + y, x * 2, '.E', curses.A_BOLD)
                elif cell == 'X':
                    stdscr.addstr(start_row + y, x * 2, '.X', curses.A_BOLD)
                elif is_solution and show_solution:
                    stdscr.addstr(start_row + y, x * 2, '·', curses.A_BOLD)
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

def main(stdscr):
    """Main function with maze configuration dictionary."""
    curses.curs_set(0)
    
    maze_config = {
        'width': 41,
        'height': 21,
        'entry_position': (1, 0),
        'exit_position': (39, 20)
    }
    
    width = maze_config['width']
    height = maze_config['height']
    entry = maze_config['entry_position']
    exit_pos = maze_config['exit_position']
    
    maze = generate_maze(width, height)
    maze[entry[1]][entry[0]] = 'E'
    maze[exit_pos[1]][exit_pos[0]] = 'X'
    
    show_solution = False
    solution_path = None
    
    draw_maze(stdscr, maze, entry, exit_pos, solution_path, show_solution)
    
    while True:
        key = stdscr.getch()
        
        if key == ord('3'):
            break
            
        elif key == ord('2'):
            if not show_solution:
                solution_path = solve_maze(maze, entry, exit_pos)
                show_solution = True
            else:
                show_solution = False
            draw_maze(stdscr, maze, entry, exit_pos, solution_path, show_solution)
            
        elif key == ord('1'):
            maze = generate_maze(width, height)
            maze[entry[1]][entry[0]] = 'E'
            maze[exit_pos[1]][exit_pos[0]] = 'X'
            show_solution = False
            solution_path = None
            draw_maze(stdscr, maze, entry, exit_pos, solution_path, show_solution)

if __name__ == '__main__':
    curses.wrapper(main)