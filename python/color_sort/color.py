from enum import Enum


class Color(Enum):
    red         = 'RE'
    green       = 'GR'
    blue        = 'BL'
    light_blue  = 'LB'
    light_green = 'LG'
    purple      = 'PU'
    fusia       = 'FU'
    grey        = 'GY'
    orange      = 'OR'
    yellow      = 'YE'
    pink        = 'PI'
    teal        = 'TE'


class ColorBox:
    def __init__(self, color, count=1):
        self.color = color
        self.count = count

    def __eq__(self, other):
        return self.color == other.color and self.count == other.count

    def dump(self):
        val = ''

        for _ in range(self.count):
            val += '|%s|\n' % self.color.value

        return val
