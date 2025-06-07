from src.components.component import BasicComponent

from reportlab.pdfgen.canvas import Canvas

class Screw(BasicComponent):
    def __init__(self, name: str, a: str, h: str, l: str | None = None):
        self.value = name
        self.type = "screw"
        self.str1 = "a = {}".format(a)
        self.str2 = "h = {}".format(h)

        if l != None:
            self.str3 = "l = {}".format(l)
        else:
            self.str3 = None

    def draw_screw_thread(self, c: Canvas, x: float, y: float, r: float, h: float) -> None:
        c.line(x - r, y, x + r, y)
        c.line(x - r, y, x - r, y - h)
        c.line(x + r, y, x + r, y - h)
        c.line(x - r, y - h, x + r, y - h)

        for i in range(3):
            c.line(x - r, y - (i + 1) * h / 3, x + r, y - i * h / 3)
    
class RecessedHeadScrew(Screw):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size, y + size, x + size, y + size)
        c.line(x - size, y + size, x - size / 2, y)
        c.line(x + size, y + size, x + size / 2, y)
        c.line(x - size / 2, y, x + size / 2, y)

        self.draw_screw_thread(c, x, y, size / 2, size)

class RoundHeadScrew(Screw):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size, y, x + size, y)
        c.line(x - size, y, x - size, y + size / 2)
        c.line(x + size, y, x + size, y + size / 2)

        c.arc(x - size, y, x + size, y + size, 0, 180)

        self.draw_screw_thread(c, x, y, size / 2, size)

class FlatHeadScrew(Screw):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        c.line(x - size, y, x + size, y)
        c.line(x - size, y, x - size, y + size)
        c.line(x + size, y, x + size, y + size)
        c.line(x - size, y + size, x + size, y + size)

        self.draw_screw_thread(c, x, y, size / 2, size)

