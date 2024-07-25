from src.components.component import BasicComponent

from reportlab.pdfgen.canvas import Canvas

class ThreadedInsert(BasicComponent):
    def __init__(self, name: str, d: str, l: str):
        self.value = name
        self.type = "insert"
        self.str1 = "d = {}".format(d)
        self.str2 = "l = {}".format(l)
        self.str3 = None

    def draw_insert(self, c: Canvas, x: float, y: float, w: float, thinw: float, h: float):
        c.line(x - w / 2, y + h / 2, x + w / 2, y + h / 2)

        for i in range(3):
            c.line(x - w / 2 + i * w / 3, y + h / 2, x - w / 2 + (i + 1) * w / 3, y + h / 6)

        c.line(x - w / 2, y + h / 2, x - w / 2, y + h / 6)
        c.line(x + w / 2, y + h / 2, x + w / 2, y + h / 6)

        c.line(x - w / 2, y + h / 6, x + w / 2, y + h / 6)
        
        c.line(x - thinw / 2, y + h / 6, x - thinw / 2, y - h / 6)
        c.line(x + thinw / 2, y + h / 6, x + thinw / 2, y - h / 6)

        c.line(x - w / 2, y - h / 6, x + w / 2, y - h / 6)
        
        for i in range(3):
            c.line(x - w / 2 + (i + 1) * w / 3, y - h / 6, x - w / 2 + i * w / 3, y - h / 2)

        c.line(x - w / 2, y - h / 2, x - w / 2, y - h / 6)
        c.line(x + w / 2, y - h / 2, x + w / 2, y - h / 6)

        c.line(x - w / 2, y - h / 2, x + w / 2, y - h / 2)

    def draw_icon(self, c: Canvas, x: float, y: float, size: float) -> None:
        self.draw_insert(c, x, y, size * 1.5, size * 1.2, size * 2)
