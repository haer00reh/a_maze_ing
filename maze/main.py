from maze.Gen import Gen
import curses
from maze.visualization import run_visualizer
from maze.resolve_conf import resolve_conf


def main() -> None:
    conf = resolve_conf()
    if len(conf) > 0:
        try:
            gen = Gen(conf, conf['entry'], conf['exit'])
            curses.wrapper(run_visualizer, gen)
        except Exception as e:
            print(f"Error: {e}")


main() if __name__ == "__main__" else None
