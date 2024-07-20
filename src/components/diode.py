from src.components.component import BasicComponent

from reportlab.lib.colors import Color
from reportlab.pdfgen.canvas import Canvas

from math import atan

class Diode(BasicComponent):
    def __init__(self, name: str, vf: str, ifwd: str, vr: str):
        self.value = name
        self.type = "diode"
        self.str1 = "Vf = {}".format(vf)
        self.str2 = "If = {}".format(ifwd)
        self.str3 = "Vr = {}".format(vr)

    def draw_diode(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size, y, x - size / 3, y)
        c.line(x + size, y, x + size / 3, y)
        
        c.line(x - size / 3, y - size / 2, x - size / 3, y + size / 2)
        c.line(x - size / 3, y - size / 2, x + size / 3, y)
        c.line(x - size / 3, y + size / 2, x + size / 3, y)

        c.line(x + size / 3, y - size / 2, x + size / 3, y + size / 2)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_diode(c, x, y, size)

class SchottkyDiode(Diode):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_diode(c, x, y, size)

        c.line(x + size / 3, y - size / 2, x + size / 3 - size / 6, y - size / 2)
        c.line(x + size / 3, y + size / 2, x + size / 3 + size / 6, y + size / 2)

class ZenerDiode(Diode):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_diode(c, x, y, size)

        c.line(x + size / 3, y - size / 2, x + size / 3 - size / 6, y - size / 2 - size / 6)
        c.line(x + size / 3, y + size / 2, x + size / 3 + size / 6, y + size / 2 + size / 6)

class LED(Diode):
    def __init__(self, name: str, vf: str, ifwd: str, wl: str, color: Color):
        self.value = name
        self.type = "diode"
        self.color = color
        self.str1 = "Vf = {}".format(vf)
        self.str2 = "If = {}".format(ifwd)
        self.str3 = "λ = {}".format(wl)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        oldcolor = c._fillColorObj

        c.setFillColor(self.color)
        path = c.beginPath()
        path.moveTo(x - size / 3, y - size / 2)
        path.lineTo(x + size / 3, y)
        path.lineTo(x - size / 3, y + size / 2)
        path.close()
        c.drawPath(path, 0, 1)

        c.setFillColor(oldcolor)

        self.draw_diode(c, x, y, size)

        self.draw_arrow(c, x + size / 2, y + size / 1.5, size / 2, size / 4, atan(2 / 1.5))
        self.draw_arrow(c, x + size, y + size / 2, size / 2, size / 4, atan(2 / 1.5))

