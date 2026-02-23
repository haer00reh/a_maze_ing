import random

class MazeGenerator:
    """Handles maze generation using depth-first search algorithm with optional 42 wall pattern."""

    @staticmethod
    def generate(width, height, entry, exit_pos):
        """Generate a maze using DFS, respecting entry and exit positions, with 42 wall block."""
        random.seed()

        # comprehension to start with a full '#' maze
        maze = [['#' for _ in range(width)] for _ in range(height)]

        # edge case for small maze input
        cells_x = (width - 1) // 2
        cells_y = (height - 1) // 2
        if cells_x < 1 or cells_y < 1:
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    maze[y][x] = ' '
            return maze

        # carve 42 pattern first
        MazeGenerator.carve_42(maze, width, height)

        # DFS starting point
        start_x, start_y = 1, 1
        maze[start_y][start_x] = ' '
        stack = [(start_x, start_y)]
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

        # DFS loop
        while stack:
            current_x, current_y = stack[-1]
            neighbors = []

            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if 1 <= new_x < width - 1 and 1 <= new_y < height - 1:
                    # Only carve into regular walls '#', not '?' cells
                    if maze[new_y][new_x] == '#':
                        # Also check the wall between current and new position
                        wall_x = current_x + dx // 2
                        wall_y = current_y + dy // 2
                        # Don't carve through '?' (aka 42 pattern walls) walls
                        if maze[wall_y][wall_x] != '?':
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

        # Connect entry and exit if at edge
        def connect_to_maze(x, y):
            maze[y][x] = ' '
            if y == 0: maze[y + 1][x] = ' '
            elif y == height - 1: maze[y - 1][x] = ' '
            elif x == 0: maze[y][x + 1] = ' '
            elif x == width - 1: maze[y][x - 1] = ' '

        connect_to_maze(*entry)
        connect_to_maze(*exit_pos)

        # small fix for even width/height
        if width % 2 == 0:
            for y in range(1, height - 1):
                if maze[y][width - 3] == ' ':
                    maze[y][width - 2] = ' '
        if height % 2 == 0:
            for x in range(1, width - 1):
                if maze[height - 3][x] == ' ':
                    maze[height - 2][x] = ' '

        return maze

    @staticmethod
    def carve_42(maze, width, height):
        """Place a solid 42 wall block in the center of the maze (if large enough)"""
        # small check if the maze is not big enough
        if width < 15 or height < 9:
            return

        center_x = width // 2
        center_y = height // 2

        # start coords for 42 (center)
        start_x = center_x - 6
        start_y = center_y - 2

        def mark_block(x, y):
            if 0 <= x < width and 0 <= y < height:
                maze[y][x] = '?'

        # drawing 4 and 2 by drawing either horizontal or vertical line for carving
        # horizontal
        for dy in range(5):
            mark_block(start_x + 4, start_y + dy)
        # vertical
        for dx in range(5):
            mark_block(start_x + dx, start_y + 2)
        # horizontal on the upper part
        for dy in range(3):
            mark_block(start_x, start_y + dy)


        offset = 7  # spacing between 4 and 2

        for dx in range(5):
            mark_block(start_x + offset + dx, start_y)
        mark_block(start_x + offset + 4, start_y + 1)
        for dx in range(5):
            mark_block(start_x + offset + dx, start_y + 2)
        mark_block(start_x + offset, start_y + 3)
        for dx in range(5):
            mark_block(start_x + offset + dx, start_y + 4)

        # Ensures a corridor between 4 and 2
        if start_x - 1 > 0:
            for dy in range(5):
                if maze[start_y + dy][start_x - 1] == '#':
                    maze[start_y + dy][start_x - 1] = ' '
        if start_x + offset + 6 < width:
            for dy in range(5):
                if maze[start_y + dy][start_x + offset + 6] == '#':
                    maze[start_y + dy][start_x + offset + 6] = ' '
