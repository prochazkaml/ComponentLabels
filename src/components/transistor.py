from src.components.component import BasicComponent

from reportlab.pdfgen.canvas import Canvas

from math import atan, pi, hypot

class BipolarJunctionTransistor(BasicComponent):
    def __init__(self, name: str, cpin: str, bpin: str, epin: str, vbe: str, ic: str, vce: str):
        self.value = name
        self.type = "BJT"
        self.str1 = "Vbe = {}".format(vbe)
        self.str2 = "Ic = {}".format(ic)
        self.str3 = "Vce = {}".format(vce)
        self.cpin = cpin
        self.bpin = bpin
        self.epin = epin

    def draw_transistor(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size / 1.5, y, x, y)
        c.line(x, y - size / 1.5, x, y + size / 1.5)

        c.line(x, y + size / 4, x + size / 1.5, y + 3 * size / 4)
        c.line(x + size / 1.5, y + 3 * size / 4, x + size / 1.5, y + size)

        c.line(x, y - size / 4, x + size / 1.5, y - 3 * size / 4)
        c.line(x + size / 1.5, y - 3 * size / 4, x + size / 1.5, y - size)

class NPNBJT(BipolarJunctionTransistor):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_transistor(c, x, y, size)
        self.draw_arrow(c, x, y - size / 4, hypot(size / 1.5, size / 2), size / 3, -atan(1.5/2))

class PNPBJT(BipolarJunctionTransistor):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_transistor(c, x, y, size)
        self.draw_arrow(c, x + size / 1.5, y + 3 * size / 4, size / 2, size / 3, atan(1.5/2) + pi)

class FieldEffectTransistor(BasicComponent):
    def __init__(self, name: str, gpin: str, dpin: str, spin: str, vgs: str, id: str, vds: str):
        self.value = name
        self.type = "FET"
        self.str1 = "Vgs = {}".format(vgs)
        self.str2 = "Id = {}".format(id)
        self.str3 = "Vds = {}".format(vds)
        self.gpin = gpin
        self.dpin = dpin
        self.spin = spin

    def draw_transistor(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size / 4, y - size / 2, x - size / 4, y + size / 2)
        
        c.line(x, y - size / 8, x, y + size / 8)
        c.line(x, y - 3 * size / 8, x, y - 5 * size / 8)
        c.line(x, y + 3 * size / 8, x, y + 5 * size / 8)

        c.line(x - size / 4, y - size / 2, x - size, y - size / 2)

        c.line(x, y + 4 * size / 8, x + 3 * size / 4, y + 4 * size / 8)
        c.line(x + 3 * size / 4, y + 4 * size / 8, x + 3 * size / 4, y + size)
        
        c.line(x, y, x + 3 * size / 4, y)

        c.line(x, y - 4 * size / 8, x + 3 * size / 4, y - 4 * size / 8)
        c.line(x + 3 * size / 4, y, x + 3 * size / 4, y - size)

class NMOSFET(FieldEffectTransistor):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_transistor(c, x, y, size)
        self.draw_arrow(c, x + 3 * size / 4, y, 3 * size / 4, size / 3, pi)

class PMOSFET(FieldEffectTransistor):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_transistor(c, x, y, size)
        self.draw_arrow(c, x, y, 3 * size / 4, size / 3, 0)

