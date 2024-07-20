from src.stickerrect import StickerRect

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, HexColor, gray
from reportlab.lib.units import inch

from typing import List
from math import pow, sin, cos, pi

class Component:
    def draw(self, c: Canvas, rect: StickerRect, draw_center_line: bool) -> None:
        raise Exception("called parent class")

    def get_value(self) -> float:
        return self.val * pow(10, self.exp - 2)

    def get_prefix(self) -> str:
        if self.exp >= 12:
            return "T"
        if self.exp >= 9:
            return "G"
        if self.exp >= 6:
            return "M"
        if self.exp >= 3:
            return "k"
        if self.exp >= 0:
            return ""
        if self.exp >= -3:
            return "m"
        if self.exp >= -6:
            return "\u03BC"
        if self.exp >= -9:
            return "n"

        return "p"

    def color_table(self, num: int) -> HexColor:
        return [
            HexColor("#000000"),
            HexColor("#964B00"),
            HexColor("#FF3030"),
            HexColor("#FFA500"),
            HexColor("#FFFF00"),
            HexColor("#00FF00"),
            HexColor("#0000FF"),
            HexColor("#C520F6"),
            HexColor("#808080"),
            HexColor("#FFFFFF"),
        ][num]

    def draw_arrow(self, c: Canvas, x: float, y: float, l: float, wl: float, a: float) -> None:
        cx = x + l * cos(a)
        cy = y + l * sin(a)

        o = pi / 5

        c.line(x, y, cx, cy)
        c.line(cx, cy, cx + wl * cos(a + pi - o), cy + wl * sin(a + pi - o))
        c.line(cx, cy, cx + wl * cos(a + pi + o), cy + wl * sin(a + pi + o))

    def draw_fancy_stripe(
        self,
        c: Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
        color_table: List[HexColor]
    ) -> None:
        c.setFillColor(color_table[2])
        c.rect(x, y+height*5/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[1])
        c.rect(x, y+height*4/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[0])
        c.rect(x, y+height*3/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[1])
        c.rect(x, y+height*2/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[2])
        c.rect(x, y+height*1/6, width, height/6, fill=1, stroke=0)
        c.setFillColor(color_table[3])
        c.rect(x, y+height*0/6, width, height/6, fill=1, stroke=0)

    def draw_stripe_border(self, c: Canvas, x: float, y: float, width: float, height: float) -> None:
        c.setLineWidth(0.3)
        c.setFillColor(black, 0.0)
        c.setStrokeColorRGB(0.2, 0.2, 0.2, 0.5)
        c.rect(x, y, width, height, fill=0, stroke=1)

    def draw_stripe(self, c: Canvas, x: float, y: float, width: float, height: float, stripe_value: int) -> None:
        if 0 <= stripe_value <= 9:
            c.setFillColor(self.color_table(stripe_value))
            c.rect(x, y, width, height, fill=1, stroke=0)
            self.draw_stripe_border(c, x, y, width, height)
            return

        elif stripe_value == -1:
            gold_table = [
                HexColor("#FFF0A0"),
                HexColor("#FFE55C"),
                HexColor("#FFD700"),
                HexColor("#D1B000"),
            ]

            self.draw_fancy_stripe(c, x, y, width, height, gold_table)
            self.draw_stripe_border(c, x, y, width, height)
            return
        elif stripe_value == -2:
            silver_table = [
                HexColor("#D0D0D0"),
                HexColor("#A9A9A9"),
                HexColor("#929292"),
                HexColor("#7B7B7B"),
            ]

            self.draw_fancy_stripe(c, x, y, width, height, silver_table)
            self.draw_stripe_border(c, x, y, width, height)
            return
        else:
            c.setLineWidth(0.5)
            c.setFillColor(gray, 0.3)
            c.setStrokeColorRGB(0.5, 0.5, 0.5, 1.0)
            c.rect(x, y, width, height, fill=1, stroke=1)
            c.line(x, y, x + width, y + height)
            c.line(x + width, y, x, y + height)
            return

    def draw_colorcode(
            self,
            c: Canvas,
            color1: object,
            color2: object,
            x: float,
            y: float,
            width: float,
            height: float,
            num_codes: int,
            exp_shift: int = 0
    ) -> None:
        exp=self.exp + exp_shift

        if exp < num_codes - 4:
            return

        border=0
        corner=0
        stripe_width=width/num_codes/2

        if self.val == 0:
            self.draw_stripe(c,
                                 x + border + corner + stripe_width / 2 + 2 * stripe_width * 2,
                                 y + border,
                                 stripe_width,
                                 height - 2 * border,
                                 0)
        else:
            for i in range(num_codes):
                if i == num_codes - 1:
                    stripe_value = exp + 2 - num_codes
                else:
                    stripe_value = self.val
                    for _ in range(2-i):
                        stripe_value //= 10
                    stripe_value %= 10

                self.draw_stripe(c,
                                     x + border + corner + stripe_width / 2 + 2 * stripe_width * i,
                                     y + border,
                                     stripe_width,
                                     height - 2 * border,
                                     stripe_value)

        c.setFillColor(black)
        c.setStrokeColor(black, 1)
        c.setLineWidth(0.5)

    def get_prefixed_number(self) -> str:
        if self.exp % 3 == 0:
            if self.val % 100 == 0:
                return str(self.val // 100)
            elif self.val % 10 == 0:
                return str(self.val // 100) + "." + str((self.val % 100) // 10)
            else:
                return str(self.val // 100) + "." + str(self.val % 100)
        elif self.exp % 3 == 1:
            if self.val % 10 == 0:
                return str(self.val // 10)
            else:
                return str(self.val // 10) + "." + str(self.val % 10)
        else:
            return str(self.val)

    def format_value(self) -> str:
        return self.get_prefixed_number() + " " + self.get_prefix() + self.units

class BasicComponent(Component):
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
        print("Generating sticker '{}' ({})".format(self.value, self.type))

        value_font_size = 0.25 * inch
        small_font_size = 0.08 * inch

        text_x = rect.left + rect.width/2 
        text_bottom = rect.bottom + rect.height/4 - value_font_size/3
        c.setFont('main', value_font_size * 1)
        c.drawCentredString(text_x, text_bottom, self.value)
        c.drawCentredString(text_x, text_bottom+rect.height/2, self.value)

        c.setFont('main', small_font_size * 1.35)
        small_text_x = rect.left + 5 * rect.width / 6
        small_text_bottom = rect.bottom + rect.height/4 - small_font_size/3

        c.setStrokeColor(black, 1)
        c.setLineWidth(2)
        c.setLineCap(1)
        
        for i in (0,rect.height/2):
            c.drawCentredString(small_text_x, i + small_text_bottom + rect.height / 8, self.str1)
            c.drawCentredString(small_text_x, i + small_text_bottom, self.str2)
            c.drawCentredString(small_text_x, i + small_text_bottom - rect.height / 8, self.str3)
            self.draw_icon(c, rect.left + rect.width / 6, rect.bottom + rect.height/4 + i, rect.height / 6)
        
        c.setLineCap(0)

