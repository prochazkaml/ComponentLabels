from reportlab.pdfgen.canvas import Canvas
from stickerrect import StickerRect

class Component:
    def draw(self, c: Canvas, rect: StickerRect, draw_center_line: bool) -> None:
        raise Exception("called parent class")

