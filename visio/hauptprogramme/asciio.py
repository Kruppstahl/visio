from asciimatics.effects import Print, Clock
from asciimatics.renderers import BarChart, FigletText, SpeechBubble, Box
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, ListBox, Layout, Text, Label, Button, \
        Background, Divider
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import math
import time
from random import randint

new_cmd = False

ROWS = 30
COLS = 80

SF_X = 0
SF_Y = 6

UHR_K_X = 54
UHR_K_Y = 0

AKT_SENDER_BOX_MAX_LENGTH = 18

def get_vol():
    return 40

def format_sl_layout(layout):
    layout.add_widget(Divider(False, 4), 0)
    layout.add_widget(Label('>>', 1), 0)

    layout.add_widget(Divider(False, 4), 2)
    layout.add_widget(Label('<<', 1), 2)

def format_pr_layout(layout):
    layout.add_widget(Label(' ', 1), 0)
    layout.add_widget(Label(' ', 1), 1)


def demo(screen):
    scenes = []
    preset_frame = Frame(screen, 11, 26, can_scroll=False, title="Tastenbelegung",
            x=SF_X, y=SF_Y, reduce_cpu=True)
    pr_layout = Layout([10, 90], fill_frame=True)
    preset_frame.add_layout(pr_layout)

    sender_frame = Frame(screen, 11, 26, can_scroll=False, title="Senderliste",
            x=27, y=6, reduce_cpu=True)
    sender_layout0 = Layout([10, 90, 10], fill_frame=True)

    sender_frame.add_layout(sender_layout0)


    optionen = [(" ", 1), ("Zweiter", 2), ("Dritter", 3), ("Vierter", 4),
            ("Deutschlandradio", 5), ("Absolut Relax", 6),
            ("Siebter", 7), ("hmm", 8)]

    sender = ["123456789012345678901", "Erster", "Zweiter", "Dritter", "Vierter", "Fünfter", "Sechster"]
    Senderkiste = ListBox(8, optionen, False)
    sender_layout0.add_widget(Senderkiste, 1)
    Senderkiste.blur()
    Senderkiste.start_line = 1

    format_sl_layout(sender_layout0)
    # format_pr_layout(pr_layout)
    for i, s in zip(range(1,6), sender):
        pr_layout.add_widget(Label(str(i), 1, align=u'^'))
        pr_layout.add_widget(Label(s, 1, align='^'), 1)


    preset_frame.fix()
    sender_frame.fix()

    effects = [preset_frame, sender_frame, 
            Print(screen, Box(26, 15, True), x=UHR_K_X, y=UHR_K_Y),
            Print(screen, Box(80, 8, True), x=0, y=17),
            Clock(screen, 67, 7, 6),
            Print(screen, FigletText("Retroradio!"), x=0, y=0),
#            Print(screen, BarChart(4, 80, [get_vol], colour=2, scale=100,
#                axes=BarChart.X_AXIS, intervals=25, labels=True, border=False), x=0, y=26,
#                transparent=False),
            # Print(screen, SpeechBubble("Lautstärke"), x=0, y=23),
            Print(screen, FigletText("Deutschlandradio"), x=1, y=18),
            Print(screen, BarChart(
                      4, 80,
                      [get_vol],
                      colour=2,
                      char=' ',
                      bg=7,
                      scale=100,
                      axes=BarChart.X_AXIS,
                      intervals=25,
                      labels=True,
                      border=False),
                  x=0, y=26, transparent=False, speed=2)]

    scenes.append(Scene(effects, -1))
    screen.play(scenes)
    

def main():
    Screen.wrapper(demo)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
