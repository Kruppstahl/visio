#!/usr/bin/python3

import json
import os
import signal
import time
import sys
from pathlib import Path

import dbus
import dbus.service
import dbus.mainloop.glib
from dbus.exceptions import DBusException
from gi.repository import GLib

from asciimatics.effects import Print, Clock
from asciimatics.renderers import BarChart, FigletText,  Box, ColourImageFile
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, ListBox, Layout,  Label, Divider
from asciimatics.screen import Screen


# Display Dimensionen
ROWS = 30
COLS = 80


AKT_SENDER_BOX_MAX_LENGTH = 18

STANDARD_CONFIG = Path('../../musiko/dateien/Debuggg.json')
NOTFALL_CONFIG = Path('./JSON_Default_Config.json')

LOGO = "../Logo/logo-test.png"

CONFIG_MEMB_AMOUNT = 20

# 6 sender above the current sender, 6 under
DISPLAY_SENDER_SYMM = 6

debug = open("debug.txt", "w")

class ASCII():
    def __init__(self):
        self.screen = Screen.open()
        self.scenes = []
        self.akt_sender_str = "Deutschlandradio"
        self.akt_sender_nr = 0
        self.volume = 25
        self.number_of_stations = 0

        # Prepare frame for the presets
        self.preset_frame = Frame(self.screen, 7, 29, can_scroll=False, 
                title="Tastenbelegung", x=0, y=10, reduce_cpu=True)
        self.pr_layout = Layout([10, 90], fill_frame=True)
        self.preset_frame.add_layout(self.pr_layout)

        # Prepare frame for the sender list
        self.sender_frame = Frame(self.screen, 17, 50, can_scroll=False,
                title="Senderliste", x=30, y=0, reduce_cpu=True)
        self.sender_layout0 = Layout([10, 80, 10], fill_frame=True)
        self.sender_frame.add_layout(self.sender_layout0)

        # Load the json config-file
        self.cfg = self.load_config()

        # Prepare the layouts, add spaces etc
        self.format_sl_layout(self.sender_layout0)

        # Nicht mehr nötig nach aktuellem Stand
        # format_pr_layout(pr_layout)

        # Create the sender-labels and fill them initially. Return them for 
        # later changing
        self.sender_labels = self.gen_and_add_sender_labels(self.sender_layout0, 
                self.parse_sender())
        self.preset_labels = self.gen_and_add_preset_labels(self.pr_layout,
                self.parse_presets())

        self.preset_frame.fix()
        self.sender_frame.fix()



    def load_config(self):
        if STANDARD_CONFIG.exists():
            with STANDARD_CONFIG.open() as f:
                konfig = json.load(f)
                print("Nutzer-Config geladen.")
        elif NOTFALL_CONFIG.exists():
            with NOTFALL_CONFIG.open() as f:
                konfig = json.load(f)
                print("Notfall-Config geladen")
        else:
            print("Katastrophaler Fehler: Keine Config-Dateien. Beende...")
            sys.exit(1)

        self.number_of_stations = len(konfig["senderliste"])
        return konfig


    # Krall Dir anhand des aktuellen Senderindizes die 6 Sendernamen vor und nach
    # dem gewählten Sender
    def parse_sender(self):
        namen = []
        j = 1

        for i in range(1, DISPLAY_SENDER_SYMM+1):
            if self.akt_sender_nr-i >= 0:
                namen.append(self.cfg["senderliste"][self.akt_sender_nr-i]
                        ["sendername"])
            else:
                index = self.number_of_stations-j
                namen.append(self.cfg["senderliste"][index]["sendername"])
                j += 1
        namen.reverse()

        for i in range(0, DISPLAY_SENDER_SYMM+1):
            namen.append(self.cfg["senderliste"][(self.akt_sender_nr+i) % 
                self.number_of_stations]["sendername"])

        for d in namen:
            debug.write(d)
        return namen


    # Hole die fünf Presets aus der Config. Setze Presets mit -1 auf den der 
    # unbelegten Taste entsprechenden Index in der Senderliste
    def parse_presets(self):
        namen = []
        for n, i in zip(self.cfg["presetliste"], range(0, 5)):
            if n >= 0:
                namen.append(self.cfg["senderliste"][n]["sendername"])
            else:
                namen.append(self.cfg["senderliste"][i]["sendername"])
                debug.write(str(i))

        return namen


    def format_sl_layout(self, layout):
        layout.add_widget(Divider(False, 7), 0)
        layout.add_widget(Label('>>>', 1, align='<'), 0)

        layout.add_widget(Divider(False, 7), 2)
        layout.add_widget(Label('<<<', 1, align='>'), 2)


    # Fülle die Senderliste initial und gib die Label für die spätere Verarbeitung
    # zurück. Die Divider bleiben als Abstandshalter dauerhaft im Layout.
    def gen_and_add_sender_labels(self, layout, namen):
        labs = []
        for name in namen:
            labs.append(Label(name, 1))

        # Add first 6 stations
        for l in labs[:DISPLAY_SENDER_SYMM]:
            layout.add_widget(l, 1)

        # Add spaces and the central station (hehe, got it?)
        layout.add_widget(Divider(False, 1), 1)
        layout.add_widget(labs[DISPLAY_SENDER_SYMM], 1)
        layout.add_widget(Divider(False, 1), 1)

        # Add the rest of the stations
        for l in labs[DISPLAY_SENDER_SYMM+1:]:
            layout.add_widget(l, 1)

        return labs


    # Füge die Spaltennummern der Presets hinzu, außerdem fülle die Presets initial
    # und gib die Liste mit den Presetlabels für die spätere Verarbeitung zurück
    def gen_and_add_preset_labels(self, layout, namen):
        preset_labs = []

        # Presetnamen einfügen in Spalte 1
        for name in namen:
            preset_labs.append(Label(name, 1))
            debug.write(name)

        for l in preset_labs:
            layout.add_widget(l, 1)

        # Spaltennummern der Presets einfügen in Spalte 0
        for i in range(1, 6):
            layout.add_widget(Label(str(i), 1), 0)

        return preset_labs


    def update_sender_labels(self):
        namen = self.parse_sender()

        for l, n in zip(self.sender_labels, namen):
            l.text = n


    def update_preset_labels(self):
        namen = parse_presets()

        for l, n in zip(self.sender_labels, namen):
            l.text = n

    def get_vol(self):
        return self.volume


    # muhahahahhahahahahaaaa!
    def asciisierer(self, s):
        tabelle = {
                ord('ä'): 'ae',
                ord('ö'): 'oe',
                ord('ü'): 'ue',
                ord('ß'): 'ss',
                ord('Ä'): 'AE',
                ord('Ö'): 'OE',
                ord('Ü'): 'UE',
                ord('ẞ'): 'SS',
                }

        return s.translate(tabelle)


    # Fill the display with the desired effects and draw the first frame
    def prepare_display(self):
        # Effects are all the stuff which will be shown on the display
        # Speed 0 means: Redraw only when draw_next_frame is executed
        effects = [self.preset_frame, self.sender_frame, 
                Print(self.screen, Box(80, 8, True), x=0, y=17, speed=0),
                Print(self.screen, ColourImageFile(self.screen, LOGO, 9, bg=7),
                    x=0, y=0, speed=0),
                Print(self.screen, FigletText(
                    self.asciisierer(self.akt_sender_str)), x=1, y=18, speed=0),
                Print(self.screen, BarChart(
                          4, 80,
                          [self.get_vol],
                          colour=2,
                          char=' ',
                          bg=7,
                          scale=100,
                          axes=BarChart.X_AXIS,
                          intervals=25,
                          labels=True,
                          border=False),
                      x=0, y=26, transparent=False, speed=0)]

        # Start displaying
        self.scenes.append(Scene(effects, -1))
        self.screen.set_scenes(self.scenes)

        # Update the screen for the first time
        self.screen.draw_next_frame()


class Bildschirm(dbus.service.Object):
    DBUS_NAME = 'hm.retro.Retro'
    DBUS_OBJECT_PATH = '/hm/retro/Retro'
    DBUS_INTERFACE = 'hm.retro.Retro'

    def __init__(self, _Visio):
        self.Visio = _Visio
        self.bus = dbus.SessionBus()
        bus_name = dbus.service.BusName(self.DBUS_NAME, bus=self.bus)

        super().__init__(bus_name, self.DBUS_OBJECT_PATH)

    @dbus.service.method(DBUS_INTERFACE, in_signature='i')
    def set_volume(self, pegel):
        self.Visio.screen.volume = pegel
        self.Visio.screen.force_update()
        self.Visio.screen.draw_next_frame()
        self.Visio.screen.refresh()

    @dbus.service.method(DBUS_INTERFACE, in_signature='i')
    def new_index(self, index):
        self.Visio.akt_sender_nr = index
        self.Visio.update_sender_labels()
        self.Visio.screen.draw_next_frame()
        self.Visio.screen.refresh()
        # self.self.screen.print_at("Hello world!", 0, 0)
        # self.self.screen.refresh()

    @dbus.service.method(DBUS_INTERFACE)
    def config_change_visio(self):
        # self.self.screen.print_at("Hello world!", 0, 0)
        # self.self.screen.refresh()
        pass

    @dbus.service.method(DBUS_INTERFACE)
    def boom(self):
        self.Visio.screen.close()
        sys.exit()


def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    loop = GLib.MainLoop()
    Visio = ASCII()
    Visio.prepare_display()

    service = Bildschirm(Visio)

    # Leg den Schalter um Igor!!!!
    loop.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
