from asciimatics.effects import Print, Clock
from asciimatics.renderers import BarChart, FigletText,  Box, ColourImageFile
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, ListBox, Layout,  Label, Divider
from asciimatics.screen import Screen

import sys
from pathlib import Path
import json

new_cmd = False

ROWS = 30
COLS = 80


AKT_SENDER_BOX_MAX_LENGTH = 18

STANDARD_CONFIG = Path('../../musiko/dateien/Debuggg.json')
NOTFALL_CONFIG = Path('../../config-dateien/JSON_Default_Config.json')

LOGO = "../Logo/logo-test.png"

CONFIG_MEMB_AMOUNT = 20

# 6 sender above the current sender, 6 under
DISPLAY_SENDER_SYMM = 6

debug = open("debug.txt", "w")


# Returns the current volume in percent
def get_vol():
    return 40


def load_config():
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

    return konfig


# Krall Dir anhand des aktuellen Senderindizes die 6 Sendernamen vor und nach
# dem gewählten Sender
def parse_sender(config, akt_nr):
    namen = []
    j = 1

    for i in range(1, DISPLAY_SENDER_SYMM+1):
        if akt_nr-i >= 0:
            namen.append(config["senderliste"][akt_nr-i]["sendername"])
        else:
            index = CONFIG_MEMB_AMOUNT-j
            namen.append(config["senderliste"][index]["sendername"])
            j += 1
    namen.reverse()

    for i in range(0, DISPLAY_SENDER_SYMM+1):
        namen.append(config["senderliste"][(akt_nr+i)%CONFIG_MEMB_AMOUNT]["sendername"])

    for d in namen:
        debug.write(d)
    return namen


# Hole die fünf Presets aus der Config. Setze Presets mit -1 auf den der 
# unbelegten Taste entsprechenden Index in der Senderliste
def parse_presets(config):
    namen = []
    for n, i in zip(config["presetliste"], range(0, 5)):
        if n >= 0:
            namen.append(config["senderliste"][n]["sendername"])
        else:
            namen.append(config["senderliste"][i]["sendername"])
            debug.write(str(i))

    return namen


def format_sl_layout(layout):
    layout.add_widget(Divider(False, 7), 0)
    layout.add_widget(Label('>>>', 1, align='<'), 0)

    layout.add_widget(Divider(False, 7), 2)
    layout.add_widget(Label('<<<', 1, align='>'), 2)


def format_pr_layout(layout):
    layout.add_widget(Label(' ', 1), 0)
    layout.add_widget(Label(' ', 1), 1)


# Fülle die Senderliste initial und gib die Label für die spätere Verarbeitung
# zurück. Die Divider bleiben als Abstandshalter dauerhaft im Layout.
def gen_and_add_sender_labels(layout, namen):
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
def gen_and_add_preset_labels(layout, namen):
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


def update_sender_labels(labs, cfg, sender_nr):
    namen = parse_sender(cfg, sender_nr)

    for l, n in zip(labs, namen):
        l.text = n


def update_preset_labels(labs, cfg):
    namen = parse_presets(cfg)

    for l, n in zip(labs, namen):
        l.text = n


# mhuhahahahhahahahahaaaa!
def asciisierer(s):
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


def run_display(screen):
    scenes = []
    AKT_SENDER = "Retro rockt!"

    # Prepare frame for the presets
    preset_frame = Frame(screen, 7, 29, can_scroll=False, title="Tastenbelegung",
            x=0, y=10, reduce_cpu=True)
    pr_layout = Layout([10, 90], fill_frame=True)
    preset_frame.add_layout(pr_layout)

    # Prepare frame for the sender list
    sender_frame = Frame(screen, 17, 50, can_scroll=False, title="Senderliste",
            x=30, y=0, reduce_cpu=True)
    sender_layout0 = Layout([10, 80, 10], fill_frame=True)
    sender_frame.add_layout(sender_layout0)

    # Load the json config-file
    cfg = load_config()

    # Prepare the layouts, add spaces etc
    format_sl_layout(sender_layout0)

    # Nicht mehr nötig nach aktuellem Stand
    # format_pr_layout(pr_layout)

    # Create the sender-labels and fill them initially. Return them for 
    # later changing
    sender_labels = gen_and_add_sender_labels(sender_layout0, parse_sender(cfg, 0))
    preset_labels = gen_and_add_preset_labels(pr_layout, parse_presets(cfg))


    preset_frame.fix()
    sender_frame.fix()

    # Effects are all the stuff which will be shown on the display
    effects = [preset_frame, sender_frame, 
            # Print(screen, Box(26, 15, True), x=54, y=0),
            Print(screen, Box(80, 8, True), x=0, y=17, speed=2),
            # Clock(screen, 68, 7, 5),
            Print(screen, ColourImageFile(screen, LOGO, 9, bg=7),
                x=0, y=0, speed=2),
            Print(screen, FigletText(asciisierer(AKT_SENDER)), x=1, y=18),
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

    # Start displaying
    scenes.append(Scene(effects, -1))
    screen.play(scenes)
    

def main():
    Screen.wrapper(run_display)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        debug.close()
        pass
