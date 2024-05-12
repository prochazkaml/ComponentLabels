from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, toColor, HexColor, gray
from reportlab.lib.units import inch
from typing import List
import math

from src.stickerrect import StickerRect
from src.components.component import Component

class Capacitor(Component):
    def __init__(self, farads: float):
        self.units = "F"

        exp = 0
        val = 0

        if farads != 0:
            # Fixed-point value with 2 decimals precision
            exp = math.floor(math.log10(farads))
            val = round(farads / math.pow(10, exp - 2))

            while val >= 1000:
                exp += 1
                val //= 10

        self.val = val
        self.exp = exp

    def get_3digit_code(self) -> str:
        if self.val % 10 != 0:
            return ""

        if self.val == 0:
            return "0"

        digits = str(self.val // 10)
        
        if self.exp == -12:
            return digits[0] + "R" + digits[1]

        if self.exp <= -2:
            multiplier = str(self.exp + 11)
            return digits + multiplier

        return ""

    def get_eia198_code(self) -> str:
        eia198_coding_table = {
            100: "A", 110: "B", 120: "C", 130: "D",
            150: "E", 160: "F", 180: "G", 200: "H",
            220: "J", 240: "K", 260: "a", 270: "L",
            300: "M", 330: "N", 350: "b", 360: "P",
            390: "Q", 400: "d", 430: "R", 450: "e",
            470: "S", 500: "f", 510: "T", 560: "U",
            600: "m", 620: "V", 680: "W", 700: "n",
            750: "X", 800: "t", 820: "Y", 900: "y",
            910: "Z"
        }

        if self.val not in eia198_coding_table:
            return ""

        digits = eia198_coding_table[self.val]

        if self.exp == -13:
            return digits + "9"
        elif self.exp <= -4:
            return digits + str(self.exp + 12)

        return ""

    def draw_capacitor(self, c: Canvas, rect: StickerRect, x: float, y: float) -> None:
        height = rect.height / 3 # / 2, but with extra margin

        size = height / 2

        c.setStrokeColor(black, 1)
        c.setLineWidth(2)

        c.line(x - size * 1.25, y, x - size / 4, y)
        c.line(x + size * 1.25, y, x + size / 4, y)
        c.line(x - size / 4, y - size, x - size / 4, y + size)
        c.line(x + size / 4, y - size, x + size / 4, y + size)

    def draw(self, c: Canvas, rect: StickerRect, draw_center_line: bool) -> None:
        # Draw middle line
        if draw_center_line:
            c.setStrokeColor(black, 0.25)
            c.setLineWidth(0.7)
            c.line(rect.left,
                   rect.bottom + rect.height/2,
                   rect.left + rect.width,
                   rect.bottom + rect.height/2)

        # Draw resistor value
        print("Generating sticker '{}'".format(self.format_value()))

        value_font_size = 0.25 * inch
        smd_font_size = 0.08 * inch
        space_between = 5

        value_string = self.format_value()
        value_width = c.stringWidth(value_string, 'Arial Bold', value_font_size * 1.35)

        text_middle = rect.left + rect.width/2
        text_bottom = rect.bottom + rect.height/4 - value_font_size/5
        c.setFont('Arial Bold', value_font_size * 1)
        c.drawCentredString(text_middle, text_bottom, value_string)
        c.drawCentredString(text_middle, text_bottom+rect.height/2, value_string)

        for bottom in (rect.bottom+rect.height/16, rect.bottom+rect.height*8/16):
            self.draw_colorcode(c,
                toColor("hsl(55, 54%, 100%)"), toColor("hsl(55, 54%, 70%)"),
                rect.left,
                bottom,
                rect.width/3, rect.height*7/16,
                3, 12)

        c.setFont('Arial Bold', smd_font_size * 1.35)
        for i in (0,rect.height/2):
            c.drawString(rect.left + rect.width / 3, rect.bottom +
                rect.height / 13 + i, self.get_3digit_code())
            c.drawRightString(rect.left + rect.width * 2 / 3, rect.bottom +
                rect.height / 13 + i, self.get_eia198_code())
            self.draw_capacitor(c, rect, rect.left + 5 * rect.width / 6, rect.bottom + rect.height/4 + i)

