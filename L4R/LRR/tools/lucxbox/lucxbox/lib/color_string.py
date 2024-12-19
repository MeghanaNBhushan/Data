from enum import Enum
from colorama import Fore, Style, init

init()


class Color(Enum):
    grey = 1
    white = 2
    red = 3
    blue = 4
    yellow = 5
    green = 6
    magenta = 7
    cyan = 8
    default = 9


def get_colored_string(raw_string, color):
    colored_string = raw_string
    if color == Color.default:
        colored_string = Fore.RESET + colored_string
    elif color == Color.grey:
        colored_string = Fore.LIGHTBLACK_EX + colored_string
    elif color == Color.white:
        colored_string = Fore.WHITE + colored_string
    elif color == Color.red:
        colored_string = Fore.LIGHTRED_EX + colored_string
    elif color == Color.blue:
        colored_string = Fore.LIGHTBLUE_EX + colored_string
    elif color == Color.yellow:
        colored_string = Fore.LIGHTYELLOW_EX + colored_string
    elif color == Color.green:
        colored_string = Fore.LIGHTGREEN_EX + colored_string
    elif color == Color.magenta:
        colored_string = Fore.LIGHTMAGENTA_EX + colored_string
    elif color == Color.cyan:
        colored_string = Fore.LIGHTCYAN_EX + colored_string

    colored_string = colored_string + Style.RESET_ALL

    return colored_string


class ColorString():
    def __init__(self, raw_string='', color=Color.default):
        if not isinstance(raw_string, str):
            raise TypeError
        self.raw = raw_string
        self.colored = get_colored_string(self.raw, color)

    def __str__(self):
        return self.colored

    def __len__(self):
        return len(self.raw)

    def __add__(self, other):
        new_color_string = ColorString()

        if isinstance(other, self.__class__):
            new_color_string.raw = self.raw + other.raw
            new_color_string.colored = self.colored + other.colored
        elif isinstance(other, str):
            new_color_string.raw = self.raw + other
            new_color_string.colored = self.colored + other
        else:
            raise TypeError

        return new_color_string

    def __radd__(self, other):
        new_color_string = ColorString()

        if isinstance(other, self.__class__):
            new_color_string.raw = other.raw + self.raw
            new_color_string.colored = other.colored + self.colored
        elif isinstance(other, str):
            new_color_string.raw = other + self.raw
            new_color_string.colored = other + self.colored
        else:
            raise TypeError

        return new_color_string

    def __mul__(self, integer):
        new_color_string = ColorString()
        new_color_string.raw = self.raw * integer
        new_color_string.colored = self.colored * integer
        return new_color_string

    __rmul__ = __mul__
