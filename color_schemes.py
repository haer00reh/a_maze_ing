import curses
COLOR_SCHEMES = {
    'Cyberpunk': {
        'entry': (curses.COLOR_CYAN, curses.COLOR_BLACK),
        'exit': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        'solution': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'walls': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'title': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
    },
    'Matrix': {
        'entry': (curses.COLOR_GREEN, curses.COLOR_BLACK),
        'exit': (curses.COLOR_GREEN, curses.COLOR_BLACK),
        'solution': (curses.COLOR_GREEN, curses.COLOR_BLACK),
        'walls': (curses.COLOR_GREEN, curses.COLOR_BLACK),
        'title': (curses.COLOR_GREEN, curses.COLOR_BLACK),
    },
    'Lava': {
        'entry': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'exit': (curses.COLOR_RED, curses.COLOR_BLACK),
        'solution': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'walls': (curses.COLOR_RED, curses.COLOR_BLACK),
        'title': (curses.COLOR_RED, curses.COLOR_BLACK),
    },
    'Deep Blue': {
        'entry': (curses.COLOR_CYAN, curses.COLOR_BLACK),
        'exit': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'solution': (curses.COLOR_WHITE, curses.COLOR_BLACK),
        'walls': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'title': (curses.COLOR_CYAN, curses.COLOR_BLACK),
    },
    'Purple': {
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
    'Midnight': {
        'entry': (curses.COLOR_CYAN, curses.COLOR_BLACK),
        'exit': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        'solution': (curses.COLOR_WHITE, curses.COLOR_BLACK),
        'walls': (curses.COLOR_BLUE, curses.COLOR_BLACK),
        'title': (curses.COLOR_CYAN, curses.COLOR_BLACK),
    },
    'Sunset': {
        'entry': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'exit': (curses.COLOR_MAGENTA, curses.COLOR_BLACK),
        'solution': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
        'walls': (curses.COLOR_RED, curses.COLOR_BLACK),
        'title': (curses.COLOR_YELLOW, curses.COLOR_BLACK),
    },
}
