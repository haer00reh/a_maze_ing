from mazegen.Gen import Gen
import curses
from mazegen.visualization import run_visualizer
from mazegen.resolve_conf import resolve_conf
import sys


def main() -> None:
    """
    main func of a_maze_ing project
        get configuration file name passed as command line
        args and parse the configs
    """
    try:
        conf = resolve_conf(sys.argv[1])
    except IndexError:
        print("Error: no config file provided!")
        return

    if len(conf) > 0:
        try:
            gen = Gen(conf, conf['entry'], conf['exit'])
            curses.wrapper(run_visualizer, gen)
        except Exception as e:
            print(f"Error: {e}")


main() if __name__ == "__main__" else None
