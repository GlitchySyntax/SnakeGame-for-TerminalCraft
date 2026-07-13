import curses

# Experimenting IGNORE THIS FILE


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(80)

    x, y = 0, 0
    while True:
        stdscr.clear()
        stdscr.addstr(y, x, "@")
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_RIGHT:
            x += 1
        elif key == curses.KEY_LEFT:
            x -= 1
        elif key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_UP:
            y -= 1


curses.wrapper(main)
