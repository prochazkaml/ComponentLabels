from src.stickerrect import StickerRect
from src.components.component import Component

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, toColor, red
from reportlab.lib.units import inch

import math

class Resistor(Component):
    def __init__(self, ohms: float, precise: bool = False):
        self.units = "\u2126"
        self.precise = precise

        exp = 0
        val = 0

        if ohms != 0:
            # Fixed-point value with 2 decimals precision
            exp = math.floor(math.log10(ohms))
            val = round(ohms / math.pow(10, exp - 2))

            while val >= 1000:
                exp += 1
                val //= 10

        self.val = val
        self.exp = exp

    def get_3digit_code(self) -> str:
        if self.val % 10 != 0:
            return ""

        if self.val == 0:
            return "000"

        digits = str(self.val // 10)

        if self.exp > 0:
            multiplier = str(self.exp - 1)
            return digits + multiplier

        if self.exp == 0:
            return digits[0] + "R" + digits[1]

        if self.exp == -1:
            return "R" + digits

        if self.exp == -2:
            if self.val % 100 != 0:
                return ""
            return "R0" + digits[0]

        return ""

    def get_4digit_code(self) -> str:
        digits = str(self.val)

        if self.val == 0:
            return "0000"

        if self.exp > 1:
            multiplier = str(self.exp - 2)
            return digits + multiplier

        if self.exp == 1:
            return digits[0] + digits[1] + "R" + digits[2]

        if self.exp == 0:
            return digits[0] + "R" + digits[1] + digits[2]

        if self.exp == -1:
            return "R" + digits

        if self.exp == -2:
            if self.val % 10 != 0:
                return ""
            return "R0" + digits[0] + digits[1]

        if self.exp == -3:
            if self.val % 100 != 0:
                return ""
            return "R00" + digits[0]

        return ""

    def get_eia98_code(self) -> str:
        eia98_coding_table = {
            100: "01", 178: "25", 316: "49", 562: "73",
            102: "02", 182: "26", 324: "50", 576: "74",
            105: "03", 187: "27", 332: "51", 590: "75",
            107: "04", 191: "28", 340: "52", 604: "76",
            110: "05", 196: "29", 348: "53", 619: "77",
            113: "06", 200: "30", 357: "54", 634: "78",
            115: "07", 205: "31", 365: "55", 649: "79",
            118: "08", 210: "32", 374: "56", 665: "80",
            121: "09", 215: "33", 383: "57", 681: "81",
            124: "10", 221: "34", 392: "58", 698: "82",
            127: "11", 226: "35", 402: "59", 715: "83",
            130: "12", 232: "36", 412: "60", 732: "84",
            133: "13", 237: "37", 422: "61", 750: "85",
            137: "14", 243: "38", 432: "62", 768: "86",
            140: "15", 249: "39", 442: "63", 787: "87",
            143: "16", 255: "40", 453: "64", 806: "88",
            147: "17", 261: "41", 464: "65", 825: "89",
            150: "18", 267: "42", 475: "66", 845: "90",
            154: "19", 274: "43", 487: "67", 866: "91",
            158: "20", 280: "44", 499: "68", 887: "92",
            162: "21", 287: "45", 511: "69", 909: "93",
            165: "22", 294: "46", 523: "70", 931: "94",
            169: "23", 301: "47", 536: "71", 953: "95",
            174: "24", 309: "48", 549: "72", 976: "96",
        }

        if self.val not in eia98_coding_table:
            return ""

        digits = eia98_coding_table[self.val]

        multiplier_table = ["Z", "Y", "X", "A", "B", "C", "D", "E", "F"]
        if not (0 <= self.exp+1 < len(multiplier_table)):
            return ""

        multiplier = multiplier_table[self.exp+1]

        return digits + multiplier

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

        value_string = self.format_value()

        text_middle = rect.left + rect.width/2
        text_bottom = rect.bottom + rect.height/4 - value_font_size/5
        c.setFont('main', value_font_size * 1)
        if self.precise:
            c.setFillColor(red)

        c.drawCentredString(text_middle, text_bottom, value_string)
        c.drawCentredString(text_middle, text_bottom+rect.height/2, value_string)
        c.setFillColor(black)

    
        # Draw resistor color code
        for bottom in (rect.bottom+rect.height/16, rect.bottom+rect.height*8/16):
            for stripes in (3,4):
                self.draw_colorcode(c,
                                        toColor("hsl(55, 54%, 100%)"), toColor("hsl(55, 54%, 70%)"),
                                        rect.left+rect.width*((stripes-3)*2/3),
                                        bottom,
                                        rect.width/3, rect.height*7/16,
                                        stripes)

        c.setFont('main', smd_font_size * 1.35)
        for i in (0,rect.height/2):
            c.drawString(rect.left + rect.width/3, rect.bottom +
                        rect.height/13+i, self.get_3digit_code())
            c.drawCentredString(rect.left + rect.width/2, rect.bottom +
                                rect.height/13+i, self.get_4digit_code())
            c.drawRightString(rect.left + rect.width*2/3, rect.bottom +
                            rect.height/13+i, self.get_eia98_code())

