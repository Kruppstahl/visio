from asciimatics.effects import Print
from asciimatics.renderers import BarChart, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import math
import time
from random import randint

new_command = False

def draw_volume(screen):
        screen.fill_polygon([[(0, 0), (10, 0), (10, 10), (0, 10)]], colour=1)
        screen.refresh()


def demo(screen):
    # while True:
        screen.print_at('X', 10, 10)
        screen.fill_polygon([[(0, 0), (10, 0), (10, 10), (0, 10)]], colour=Screen.COLOUR_GREEN)
        screen.refresh()

        while not new_command:
            time.sleep(0.04)


def main():
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
