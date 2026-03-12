pp = poetry
py = python3

run:
	@${pp} run $(py) a_maze_ing.py config.txt

install:
	@pip install poetry
	@$(pp) install

build:
	pip install build
	python -m build
debug:
	@${pp} run ${py} -m pdb a_maze_ing.py config.txt


clean:
	@rm -rf */__pycache__
	@rm -rf .mypy_cache
	@rm -rf mazegen/.mypy_cache
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean_all: clean
	@$(pp) env remove
	@echo "to remove poetry u can run:"
	@echo "|-- pip uninstall poetry"

