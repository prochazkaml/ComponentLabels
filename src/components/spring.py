from src.components.component import BasicComponent

from reportlab.pdfgen.canvas import Canvas

class Spring(BasicComponent):
    def __init__(self, d: str, l: str):
        self.value = l
        self.type = "spring"
        self.str1 = "d = {}".format(d)
        self.str2 = None
        self.str3 = None

    def draw_spring(self, c: Canvas, x: float, y: float, w: float, h: float, loops: int):
        for i in range(loops):
            c.line(x - w / 2, y - h / 2 + i * h / loops, x + w / 2, y - h / 2 + (i + 1) * h / loops)

        for i in range(loops + 1):
            c.line(x - w / 2, y - h / 2 + i * h / loops, x + w / 2, y - h / 2 + i * h / loops)

class CompressionSpring(Spring):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_spring(c, x, y, size * 1.5, size * 2, 4)

class ExtensionSpring(Spring):
    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_spring(c, x, y, size * 1.5, size, 2)
        c.circle(x - size * .75, y + size / 2 + size / 4, size / 4)
        c.circle(x + size * .75, y - size / 2 - size / 4, size / 4)

