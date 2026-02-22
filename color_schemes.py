import curses
COLOR_SCHEMES = {
    'Blue': {
        'entry': (curses.COLOR_CYAN, curses.COLOR_BLACK),
        'exit': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        'solution': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'walls': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'title': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
    },
    'red': {
        'entry': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'exit': (curses.COLOR_RED, curses.COLOR_BLACK),
        'solution': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'walls': (curses.COLOR_RED, curses.COLOR_BLACK),
        'title': (curses.COLOR_RED, curses.COLOR_BLACK),
    },
    'Graphite': {
        'entry': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'exit': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'solution': (curses.COLOR_WHITE, curses.COLOR_BLACK),
        'walls': (curses.COLOR_BLACK, curses.COLOR_WHITE),
        'title': (curses.COLOR_CYAN, curses.COLOR_BLACK),
    },
    'Pink': {
        'entry': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'exit': (curses.COLOR_RED, curses.COLOR_BLACK),
        'solution': (curses.COLOR_WHITE, curses.COLOR_BLACK),
        'walls': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        'title': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
    },
    'Emerald': {
        'entry': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'exit': (curses.COLOR_RED, curses.COLOR_BLACK),
        'solution': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'walls': (curses.COLOR_GREEN, curses.COLOR_BLACK),
        'title': (curses.COLOR_GREEN, curses.COLOR_BLACK),
    },
    'Orange': {
        'entry': (curses.COLOR_CYAN, curses.COLOR_BLACK),
        'exit': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        'solution': (curses.COLOR_WHITE, curses.COLOR_BLACK),
        'walls': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'title': (curses.COLOR_CYAN, curses.COLOR_BLACK),
    }
}
