from asciimatics.effects import Print
from asciimatics.renderers import BarChart, FigletText, Renderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import math
import time
from random import randint


def get_volume():
    return 40


def wv(x):
    return lambda: 1 + math.sin(math.pi * (2*time.time()+x) / 5)


def demo(screen):
    scenes = []
    effects = [
        Print(screen,
              BarChart(5, 80, [get_volume],
                       char="=",
                       gradient=[(20, Screen.COLOUR_GREEN),
                                 (30, Screen.COLOUR_YELLOW),
                                 (40, Screen.COLOUR_RED)]),
              x=13, y=1, transparent=False, speed=2),
    ]

    scenes.append(Scene(effects, -1))
    screen.print_at("hihihihi", 10, 10)
    screen.play(scenes, stop_on_resize=True)


while True:
    try:
        Screen.wrapper(demo)
        sys.exit(0)
    except ResizeScreenError:
        pass
