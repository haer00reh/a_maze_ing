import random


class MazeGenerator:
    """Handles maze generation using depth-first search algorithm."""
    
    @staticmethod
    def generate(width, height, entry, exit_pos):
        """Generate a maze using depth-first search algorithm."""
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
        
        exit_y = None
        for y in range(height - 2, 1, -1):
            if maze[y][width - 3] == ' ':
                exit_y = y
                break
        
        if exit_y is None:
            exit_y = height - 2
        
        exit_x = width - 2
        
        maze[exit_y][exit_x] = ' '
        
        for dy in [-1, 0, 1]:
            for dx in [-1, 0]:
                y = exit_y + dy
                x = exit_x + dx
                if 0 < y < height - 1 and 0 < x < width - 1:
                    maze[y][x] = ' '
        
        if width % 2 == 0:
            for y in range(1, height - 1):
                if maze[y][width - 3] == ' ':
                    maze[y][width - 2] = ' '
        
        if height % 2 == 0:
            for x in range(1, width - 1):
                if maze[height - 3][x] == ' ':
                    maze[height - 2][x] = ' '
        
        def connect_to_maze(x, y):
            if y == 0:
                maze[y][x] = ' '
                maze[y + 1][x] = ' '
            elif y == height - 1:
                maze[y][x] = ' '
                maze[y - 1][x] = ' '
            elif x == 0:
                maze[y][x] = ' '
                maze[y][x + 1] = ' '
            elif x == width - 1:
                maze[y][x] = ' '
                maze[y][x - 1] = ' '
        
        connect_to_maze(*entry)
        connect_to_maze(*exit_pos)
        return maze