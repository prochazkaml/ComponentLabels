from reportlab.pdfgen.canvas import Canvas

from src.components.component import BasicComponent

from math import sin, cos, pi

class Nut(BasicComponent):
    def __init__(self, name: str, m: str, s: str, d: str):
        self.value = name
        self.type = "nut"
        self.str1 = "m = {}".format(m)
        self.str2 = "s = {}".format(s)
        self.str3 = "d = {}".format(d)

class HexNut(Nut):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        for i in range(6):
            c.line(x + cos(i * pi / 3) * size, y + sin(i * pi / 3) * size, x + cos((i + 1) * pi / 3) * size, y + sin((i + 1) * pi / 3) * size)
        
        c.circle(x, y, size / 2)

class SquareNut(Nut):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size, y - size, x + size, y - size)
        c.line(x + size, y - size, x + size, y + size)
        c.line(x + size, y + size, x - size, y + size)
        c.line(x - size, y + size, x - size, y - size)

        c.circle(x, y, size / 2)

