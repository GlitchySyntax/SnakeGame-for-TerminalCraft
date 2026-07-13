"""
Terminal Snake — For TerminalCraft

Controls:
  Arrow keys / WASD  - move
  p                   - pause / unpause
  q                   - quit

Run with:  python3 snake.py
Built on Arch Linux (The superior Operating System >:) )
"""

import curses
import random


def main(stdscr):
    # setup
    curses.curs_set(0)  # hide the blinking cursor or not
    stdscr.nodelay(True)  # getch() doesn't block
    stdscr.timeout(80)  # game speed: ms between frames

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # da snek
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # fud
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # UI text
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # border

    sh, sw = stdscr.getmaxyx()  # screen height / width
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(True)
    win.timeout(100)

    play_again = True

    while play_again:
        play_again = run_game(win, sh, sw)

    curses.curs_set(
        1
    )  # restore cursor on the way out otherwise a VIM moment will happen


def run_game(win, sh, sw):
    """Plays one round of snake. Returns True if the player wants to replay."""

    # initialising the snek
    snake = [
        [sh // 2, sw // 4],
        [sh // 2, sw // 4 - 1],
        [sh // 2, sw // 4 - 2],
        [sh // 2, sw // 4 - 3],
        [sh // 2, sw // 4 - 4],
    ]
    direction = curses.KEY_RIGHT

    food = spawn_food(snake, sh, sw)
    score = 0
    paused = False

    while True:
        win.clear()
        draw_border(win, sh, sw)
        draw_score(win, sw, score)

        # da fud
        win.addch(food[0], food[1], "*", curses.color_pair(2) | curses.A_BOLD)

        # da snek
        for i, (y, x) in enumerate(snake):
            char = "@" if i == 0 else "o"
            win.addch(y, x, char, curses.color_pair(1) | curses.A_BOLD)

        win.refresh()

        # User input
        key = win.getch()

        if key == ord("q"):
            return False

        if key == ord("p"):
            paused = not paused

        if paused:
            show_message(win, sh, sw, "PAUSED — press p to resume")
            continue

        new_direction = key_to_direction(key)
        if new_direction is not None and not is_reverse(direction, new_direction):
            direction = new_direction

        # Da snek actually moving
        head_y, head_x = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head_y, head_x + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head_y, head_x - 1]
        elif direction == curses.KEY_UP:
            new_head = [head_y - 1, head_x]
        else:  #
            new_head = [head_y + 1, head_x]

        # Collision checs/Check if sneck ded
        if (
            new_head[0] in (0, sh - 1)
            or new_head[1] in (0, sw - 1)
            or new_head in snake
        ):
            return game_over_screen(win, sh, sw, score)

        snake.insert(0, new_head)

        if new_head == food:
            score += 10
            food = spawn_food(snake, sh, sw)
            win.timeout(max(40, 100 - score // 2))  # speed up slowly
        else:
            snake.pop()


def key_to_direction(key):
    mapping = {
        curses.KEY_RIGHT: curses.KEY_RIGHT,
        curses.KEY_LEFT: curses.KEY_LEFT,
        curses.KEY_UP: curses.KEY_UP,
        curses.KEY_DOWN: curses.KEY_DOWN,
        ord("d"): curses.KEY_RIGHT,
        ord("a"): curses.KEY_LEFT,
        ord("w"): curses.KEY_UP,
        ord("s"): curses.KEY_DOWN,
    }
    return mapping.get(key)


def is_reverse(current, new):
    opposites = {
        curses.KEY_RIGHT: curses.KEY_LEFT,
        curses.KEY_LEFT: curses.KEY_RIGHT,
        curses.KEY_UP: curses.KEY_DOWN,
        curses.KEY_DOWN: curses.KEY_UP,
    }
    return opposites.get(current) == new


def spawn_food(snake, sh, sw):
    while True:
        pos = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
        if pos not in snake:
            return pos


def draw_border(win, sh, sw):
    win.attron(curses.color_pair(4))
    win.border()
    win.attroff(curses.color_pair(4))


def draw_score(win, sw, score):
    text = f" Score: {score} "
    win.addstr(
        0, max(1, sw - len(text) - 2), text, curses.color_pair(3) | curses.A_BOLD
    )


def show_message(win, sh, sw, text):
    y, x = sh // 2, max(1, (sw - len(text)) // 2)
    win.addstr(y, x, text, curses.color_pair(3) | curses.A_BOLD)
    win.refresh()


def game_over_screen(win, sh, sw, score):
    win.nodelay(False)  # await key press
    lines = [
        "GAME OVER",
        "Snek ded :(",
        f"Final score: {score}",
        "",
        "Press r to play again, or q to quit",
    ]
    start_y = sh // 2 - len(lines) // 2
    win.clear()
    draw_border(win, sh, sw)
    for i, line in enumerate(lines):
        x = max(1, (sw - len(line)) // 2)
        attr = curses.color_pair(2) | curses.A_BOLD if i == 0 else curses.color_pair(3)
        win.addstr(start_y + i, x, line, attr)
    win.refresh()

    while True:
        key = win.getch()
        if key == ord("r"):
            win.nodelay(True)
            win.timeout(100)
            return True
        if key == ord("q"):
            return False


if __name__ == "__main__":
    curses.wrapper(main)
