# A-Maze-ing

A sophisticated maze generation and solving application built with Python, featuring multiple algorithms and an interactive terminal-based interface.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Algorithms](#algorithms)
- [Controls](#controls)
- [Project Structure](#project-structure)
- [Team](#team)
- [Resources](#resources)
- [License](#license)

## Overview

This project has been created as part of the 42 curriculum by **haer-reh** and **amerkht**.

A-Maze-ing is an interactive maze generation and solving tool that implements multiple pathfinding algorithms. The project features a clean, colorful terminal interface powered by the `curses` library, allowing users to generate mazes, visualize algorithms in real-time, and solve mazes using different strategies.

## Features

- **Multiple Maze Generation Algorithms**: BFS (Breadth-First Search) and DFS (Depth-First Search)
- **Real-time Algorithm Visualization**: Watch as the maze is generated and solved step-by-step
- **8 Color Schemes**: Toggle between 8 distinct color themes for personalized visualization
- **Interactive Controls**: Intuitive keyboard controls for maze manipulation
- **Imperfect Maze Generation**: Create mazes with multiple paths and loops
- **Configurable Parameters**: Customize maze dimensions, speed, and behavior via config file
- **Modular Design**: Reusable `mazegen` package for integration into other projects
- **Clean Terminal UI**: Professional text-based interface using curses

## Installation

### Prerequisites
- Python 3.x
- Unix-like environment (Linux, macOS, WSL)

### Setup
```bash
# Clone the repository
git clone <repository-url>

# Install dependencies (if using pip)
poetry install

# Or using make
make install
```

## 📖 Usage

### Basic Usage
```bash
make run # run the application
clean_all # clean build artifacts and run the application
clean # remove build artifacts
build # build the project using pip
install # build and install the project using poetry
```

### Usage Examples

**Generate a DFS maze:**
1. Launch the application
2. Press `d` to generate using Depth-First Search
3. Watch the algorithm create the maze in real-time

**Solve the maze:**
1. After generating a maze
2. Press `s` to solve using DFS algorithm
3. The solution path will be highlighted

**Change color scheme:**
- Press keys `1` through `8` to cycle through different color themes

**Reset the maze:**
- Press `r` to clear and reset the current maze

## ⚙️ Configuration

Edit `config.txt` to customize maze parameters:
- Maze dimensions (width/height)
- Animation speed
- Starting/ending positions
- Generation preferences

## Algorithms

### Maze Generation Algorithms

#### Depth-First Search (DFS)
- **Description**: Creates mazes using recursive backtracking
- **Characteristics**: Produces long, winding corridors with fewer branches
- **Why we chose it**: Excellent for understanding backtracking concepts and their relation to maze generation. Creates more challenging mazes with complex paths.

#### Breadth-First Search (BFS)
- **Description**: Generates mazes by exploring all neighboring cells level by level
- **Characteristics**: Creates mazes with more uniform corridor lengths
- **Why we chose it**: Demonstrates graph traversal techniques and systematic cell exploration. Helps understand how BFS explores all possibilities at each depth.

### Maze Solving Algorithm
- **DFS-based solver**: Finds a path from entry to exit using depth-first traversal

## Controls

| Key | Action |
|-----|--------|
| `1-8` | Toggle between maze color schemes |
| `d` | Generate maze using DFS algorithm |
| `b` | Generate maze using BFS algorithm |
| `s` | Solve the current maze using DFS |
| `r` | Reset/clear the maze |
| `q` | Quit the application |

## 📁 Project Structure

```
a_maze_ing/
├── a_maze_ing.py          # Main application entry point
├── config.txt             # Configuration file
├── Makefile               # Build and run commands
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # This file
└── mazegen/               # Core maze generation package
    ├── __init__.py        # Package initialization
    ├── Cell.py            # Cell data structure
    ├── Gen.py             # Maze generation algorithms
    ├── Parsing.py         # Configuration parsing
    ├── resolve_conf.py    # Configuration resolution
    ├── color_schemes.py   # Color scheme definitions
    ├── visualization.py   # Rendering and display logic
    ├── helpers.py         # Utility functions
    └── Errors.py          # Custom exception classes
```

## Reusability

The **`mazegen` package** is designed to be modular and reusable:
- Import it into other Python projects
- Use the maze generation algorithms independently
- Customize visualization for different interfaces
- Extend with additional algorithms

Example:
```python
from mazegen import Gen, Cell

# Use in your own project
maze = Gen.create_maze(width=50, height=25)
```

## 👥 Team

### Contributors & Roles

**haer-reh**
- Visualization & rendering (terminal interface, colors, UI/UX)
- Partial maze generation implementation
- Imperfect maze generation feature

**amerkht**
- Algorithm implementation (DFS, BFS)
- Configuration parsing system
- Code structure and architecture
- 42 pattern implementation

## 📚 Resources

- [Python Curses Documentation](https://docs.python.org/3/howto/curses.html)
- [Breadth-First Traversal Tutorial](https://www.tutorialspoint.com/data_structures_algorithms/breadth_first_traversal.htm)
- [Depth-First Search Algorithm](https://www.codecademy.com/article/depth-first-search-dfs-algorithm)

## AI Usage Disclosure

AI was used for debugging and gathering information/knowledge. No code decisions or implementations were done using AI. All algorithmic logic and design decisions were made by the team members.

## 🛠️ Tools & Technologies

- **Python 3**: Core programming language
- **curses**: Terminal-based UI library for clean text interface
- **Custom data structures**: Cell representation and maze graph

## License

This project is part of the 42 curriculum.

---

*Created with collaboration by haer-reh and amerkht*