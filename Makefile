all:
	python3 -m maze.a_maze_ing


clean:
	@rm -rf */__pycache__
	@rm -rf .mypy_cache
