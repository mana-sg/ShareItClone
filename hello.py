import curses
import time


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    while True:
        # Get current time
        current_time = time.strftime("%H:%M:%S", time.localtime())

        # Clear the screen
        stdscr.clear()

        # Add content to the screen
        stdscr.addstr(0, 0, "Current Time: {}".format(current_time))

        # Refresh the screen to update the displayed content
        stdscr.refresh()

        # Wait for a short duration before updating again
        time.sleep(1)


if __name__ == "__main__":
    curses.wrapper(main)
