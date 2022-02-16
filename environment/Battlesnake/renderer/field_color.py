# Colors
# 000000 / (0,     0,   0) (schwarz)
# 55415f / (85,   65,  95) (lila)
# 646964 / (100, 105, 100) (grau)
# d77355 / (215, 115,  85) (rot)
# 508cd7 / (80,  140, 215) (blau)
# 64b964 / (100, 185, 100) (grün)
# e6c86e / (230, 200, 110) (gelb)
# dcf5ff / (220, 245, 255) (weiß)

colors = [
    "#a100f2",
    "#7bdff2",
    "#b58db6",
    "#16db93",
    "#5a83ed",
    "#f1c453",
    "#f29e4c",
    "#fe5f55",
    "#83e377",
    "#fb6376",
    "#0db39e",
    "#495867",
    "#78290f",
]


def hexToRGB(hex_val):
    h = hex_val.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


class FieldColor:
    # Field color (red, green, blue)

    SNAKE_1_DEFAULT = (80, 140, 215)
    SNAKE_2_DEFAULT = (100, 185, 100)
    SNAKE_3_DEFAULT = (230, 200, 110)
    SNAKE_4_DEFAULT = (85, 65, 95)
    food = (215, 115, 85)
    background = (100, 105, 100)
    hazard = (43, 45, 43)
    SNAKE_COLORS = [hexToRGB(c) for c in colors]

