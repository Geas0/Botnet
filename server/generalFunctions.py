import json

ALLOWED_CHARACTERS = (
    "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h",
    "j", "k", "l", "z", "x", "c", "v", "b", "n", "m", "Q", "W", "E", "R", "T", "Y",
    "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C",
    "V", "B", "N", "M", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."
)

def detect_lfi(file):
    # Detecting LFI trought whitelist
    for c in file:
        if not c in ALLOWED_CHARACTERS:
            return True # Lfi
    
    return False # Not lfi


def get_config():
    # Reading config.json file
    with open("../config.json", "r") as f:
        config = json.load(f)

    return config