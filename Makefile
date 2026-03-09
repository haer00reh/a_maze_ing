pp = poetry
py = python3

run:
	@${pp} run $(py) a_maze_ing.py config.txt

install:
	@pip install poetry
	@$(pp) install

clean:
	@rm -rf */__pycache__
	@rm -rf .mypy_cache
