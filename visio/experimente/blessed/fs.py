from __future__ import division
from blessed import Terminal

term = Terminal()
with term.fullscreen():
    print(term.move_y(term.height // 2) +
          term.center('press any key').rstrip())
    term.inkey()
