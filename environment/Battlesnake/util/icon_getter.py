import os
from pygame import image, Surface

available_heads = [
    "all-seeing",
    "bonhomme",
    "bwc-snow-worm",
    "default",
    "happy",
    "moto-helmet",
    "rbc-bowler",
    "scarf",
    "silly",
    "snowman",
    "whale",
    "alligator",
    "bwc-bonhomme",
    "bwc-snowman",
    "earmuffs",
    "iguana",
    "moustache",
    "regular",
    "shac-caffeine",
    "ski",
    "space-helmet",
    "workout",
    "beluga",
    "bwc-earmuffs",
    "caffeine",
    "evil",
    "jackolantern",
    "orca",
    "replit-mark",
    "shac-gamer",
    "smile",
    "tiger-king",
    "bendr",
    "bwc-rudolph",
    "chomp",
    "fang",
    "lantern-fish",
    "pixel-round",
    "rudolph",
    "shac-tiger-king",
    "snail",
    "tongue",
    "bfl-jackolantern",
    "bwc-scarf",
    "comet",
    "football",
    "mask",
    "pixel",
    "safe",
    "shac-workout",
    "sneaky",
    "villain",
    "bfl-pumpkin",
    "bwc-ski",
    "dead",
    "gamer",
    "missile",
    "pumpkin",
    "sand-worm",
    "shades",
    "snow-worm",
    "viper"]

available_tails = [
    "alligator",
    "bonhomme",
    "bwc-present",
    "default",
    "football",
    "ice-skate",
    "missile",
    "pixel",
    "regular",
    "shac-mouse",
    "shiny",
    "snail",
    "tire",
    "bfl-leaf",
    "bwc-bonhomme",
    "coffee",
    "fat-rattle",
    "freckled",
    "iguana",
    "mouse",
    "present",
    "replit-notmark",
    "shac-tiger-tail",
    "skinny-jeans",
    "swirl",
    "virus",
    "block-bum",
    "bwc-flake",
    "comet",
    "fish",
    "ghost",
    "ion",
    "offroad",
    "rattle",
    "round-bum",
    "shac-weight",
    "skinny",
    "swoop",
    "weight",
    "bolt",
    "bwc-ice-skate",
    "curled",
    "flake",
    "hook",
    "leaf",
    "pixel-round",
    "rbc-necktie",
    "shac-coffee",
    "sharp",
    "small-rattle",
    "tiger-tail"]

def get_head_from_assets(name: str) -> Surface:
    """ Returns a head (as png) from local assets.
        Only assets from the official Repo are available.
        https://github.com/BattlesnakeOfficial/exporter/tree/main/render/assets"""

    if name is None or name not in available_heads:
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heads/default.png")
    else:
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"heads/{name}.png")

    surface = image.load(image_path)
    surface = surface.convert_alpha()
    return surface

def get_tail_from_assets(name: str) -> Surface:
    """ Returns a tail (as png) from local assets.
        Only assets from the official Repo are available.
        https://github.com/BattlesnakeOfficial/exporter/tree/main/render/assets"""
    
    if name is None or name not in available_tails:
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tails/default.png")
    else:
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"tails/{name}.png")

    surface = image.load(image_path)
    surface = surface.convert_alpha()
    return surface