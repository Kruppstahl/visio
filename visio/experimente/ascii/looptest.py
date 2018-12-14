from asciimatics.effects import Print
from asciimatics.renderers import BarChart, FigletText
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, ListBox, Layout, Text, Label, Button, \
        Background
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import math
import time
from random import randint

new_cmd = False

def demo(screen):
    scenes = []
    frame = Frame(screen, 20, 80, can_scroll=False, title="Sender")
    layout = Layout([40, 10, 40, 10], fill_frame=True)
    frame.add_layout(layout)

    optionen = [("Erster", 1), ("Zweiter", 2)]

    sender = ["Erster hihihihihihi", "Zweiter", "Dritter"]

    for s in sender:
        layout.add_widget(Label(s, align=u'^'))

    layout.add_widget(Label("<<<<", align='<'), 1)

    layout.add_widget(Button("hihi!", None))

    frame.fix()

    effects = [frame]

    scenes.append(Scene(effects, -1))
    screen.play(scenes)
    

def main():
    Screen.wrapper(demo)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
