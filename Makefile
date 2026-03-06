all:
	python3 -m maze.main


clean:
	@rm -rf */__pycache__
	@rm -rf .mypy_cache
