import urwid

txt = urwid.Text(u"Hello World")
fill = urwid.Filler(txt, ('relative', 40))
loop = urwid.MainLoop(fill)
loop.run()
