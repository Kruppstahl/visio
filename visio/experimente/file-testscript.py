import json
import sys
from pathlib import Path

STANDARD_CONFIG = Path('../../musiko/dateien/Beispiel_neuester_Standard.json')
NOTFALL_CONFIG = Path('../../musiko/dateien/config2.json')

def get_vol():
    return 40

def load_config():
    if STANDARD_CONFIG.exists():
        with STANDARD_CONFIG.open() as f:
            konfig = json.load(f)
            print("User-Config geladen.")
    elif NOTFALL_CONFIG.exists():
        with NOTFALL_CONFIG.open() as f:
            konfig = json.load(f)
            print("Notfall-Config geladen")
    else:
        print("Katastrophaler Fehler: Keine Config-Dateien. Beende...")
        sys.exit(1)

    return konfig

def parse_config(config, akt_nr):
    namen = []
    for i in range(-7, 8):
        print( (config["senderliste"][(akt_nr+i)%10]["sendername"], i) )

    return namen

cfg = load_config()
namen = parse_config(cfg, 2)

for elm in namen:
    print(elm)
