#!/usr/bin/env python3

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.lib.colors import black, toColor, HexColor, gray

import math
import sys

from typing import Tuple, Union, Optional, List


def load_font(font_name: str) -> None:
    pdfmetrics.registerFont(TTFont('Arial Bold', font_name))
    print("Using font '{}' ...".format(font_name))


if "--noroboto" not in sys.argv:
    try:
        load_font('Roboto-Bold.ttf')
    except TTFError as e:
        print("Error: {}".format(e))
        exit(1)

else:
    for font_name in ['ArialBd.ttf', 'Arial_Bold.ttf']:
        try:
            load_font(font_name)
            break
        except TTFError:
            pass
    else:
        print("Error: Unable to load font 'Arial Bold'.")
        print("If you are on Ubuntu, you can install it with:")
        print("    sudo apt install ttf-mscorefonts-installer")
        print("Alternatively, use the 'Roboto' font by invoking this script with")
        print("the '--roboto' flag.")
        print("On Mac OS the '--roboto' flag is mandatory because this script currently")
        print("does not support Arial on Mac OS.")
        exit(1)


class PaperConfig:
    def __init__(
        self,
        paper_name: str,
        pagesize: Tuple[float, float],
        sticker_width: float,
        sticker_height: float,
        sticker_corner_radius: float,
        left_margin: float,
        top_margin: float,
        horizontal_stride: float,
        vertical_stride: float,
        num_stickers_horizontal: int,
        num_stickers_vertical: int,
    ) -> None:
        self.paper_name = paper_name
        self.pagesize = pagesize
        self.sticker_width = sticker_width
        self.sticker_height = sticker_height
        self.sticker_corner_radius = sticker_corner_radius
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.horizontal_stride = horizontal_stride
        self.vertical_stride = vertical_stride
        self.num_stickers_horizontal = num_stickers_horizontal
        self.num_stickers_vertical = num_stickers_vertical


AVERY_5260 = PaperConfig(
    paper_name="Avery 5260",
    pagesize=LETTER,
    sticker_width=(2 + 5/8) * inch,
    sticker_height=1 * inch,
    sticker_corner_radius=0.1 * inch,
    left_margin=3/16 * inch,
    top_margin=0.5 * inch,
    horizontal_stride=(2 + 6/8) * inch,
    vertical_stride=1 * inch,
    num_stickers_horizontal=3,
    num_stickers_vertical=10,
)


AVERY_L7157 = PaperConfig(
    paper_name="Avery L7157",
    pagesize=A4,
    sticker_width=64 * mm,
    sticker_height=24.3 * mm,
    sticker_corner_radius=3 * mm,
    left_margin=6.4 * mm,
    top_margin=14.1 * mm,
    horizontal_stride=66.552 * mm,
    vertical_stride=24.3 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=11,
)


EJ_RANGE_24 = PaperConfig(
    paper_name="EJRange 24",
    pagesize=A4,
    sticker_width=63.5 * mm,
    sticker_height=33.9 * mm,
    sticker_corner_radius=2 * mm,
    left_margin=6.5 * mm,
    top_margin=13.2 * mm,
    horizontal_stride=66.45 * mm,
    vertical_stride=33.9 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=8,
)


VYSOCINA = PaperConfig( # Available from: https://www.obalyvysocina.cz/produkty/samolepici-etikety#70x254-mm3300-ks
    paper_name="Samolepky z Vysočiny",
    pagesize=A4,
    sticker_width=62 * mm,
    sticker_height=24 * mm,
    sticker_corner_radius=0,
    left_margin=4 * mm,
    top_margin=8.8 * mm,
    horizontal_stride=70 * mm,
    vertical_stride=25.4 * mm,
    num_stickers_horizontal=3,
    num_stickers_vertical=11
)


class StickerRect:
    def __init__(self, c: Canvas, layout: PaperConfig, row: int, column: int, mirror: bool):
        self.left = layout.left_margin + layout.horizontal_stride * column
        self.bottom = layout.pagesize[1] - (
            layout.sticker_height + layout.top_margin + layout.vertical_stride * row
        )
        self.width = layout.sticker_width
        self.height = layout.sticker_height
        self.corner = layout.sticker_corner_radius

        self._mirror = mirror
        self._c = c

    def __enter__(self) -> "StickerRect":

        if self._mirror:
            pagewidth = self._c._pagesize[0]
            pageheight = self._c._pagesize[1]
            self._c.saveState()
            self._c.translate(pagewidth, pageheight)
            self._c.rotate(180)
            self.left = pagewidth - self.left - self.width
            self.bottom = pageheight - self.bottom - self.height

        return self

    def __exit__(self, _type: object, _value: object, _traceback: object) -> None:
        if self._mirror:
            self._c.restoreState()


class Component:
    def draw(self, c: Canvas, rect: StickerRect, draw_center_line: bool) -> None:
        raise Exception("called parent class")


class Resistor(Component):
    def __init__(self, ohms: float):
        ohms_exp = 0
        ohms_val = 0

        if ohms != 0:
            # Fixed-point value with 2 decimals precision
            ohms_exp = math.floor(math.log10(ohms))
            ohms_val = round(ohms / math.pow(10, ohms_exp - 2))

            while ohms_val >= 1000:
                ohms_exp += 1
                ohms_val //= 10

        self.ohms_val = ohms_val
        self.ohms_exp = ohms_exp

        # print(self.ohms_val, self.ohms_exp, self.format_value(), self.get_value())

    def get_value(self) -> float:
        return self.ohms_val * math.pow(10, self.ohms_exp - 2)

    def get_prefix(self) -> str:
        if self.ohms_exp >= 12:
            return "T"
        if self.ohms_exp >= 9:
            return "G"
        if self.ohms_exp >= 6:
            return "M"
        if self.ohms_exp >= 3:
            return "k"
        if self.ohms_exp >= 0:
            return ""
        if self.ohms_exp >= -3:
            return "m"
        if self.ohms_exp >= -6:
            return "\u03BC"
        return "n"

    def get_prefixed_number(self) -> str:
        if self.ohms_exp % 3 == 0:
            if self.ohms_val % 100 == 0:
                return str(self.ohms_val // 100)
            elif self.ohms_val % 10 == 0:
                return str(self.ohms_val // 100) + "." + str((self.ohms_val % 100) // 10)
            else:
                return str(self.ohms_val // 100) + "." + str(self.ohms_val % 100)
        elif self.ohms_exp % 3 == 1:
            if self.ohms_val % 10 == 0:
                return str(self.ohms_val // 10)
            else:
                return str(self.ohms_val // 10) + "." + str(self.ohms_val % 10)
        else:
            return str(self.ohms_val)

    def format_value(self) -> str:
        if self.ohms_exp < 0:
            rendered_num = str(self.ohms_val)
            while rendered_num[-1] == "0":
                rendered_num = rendered_num[:-1]
            if self.ohms_exp == -1:
                return "0." + rendered_num
            if self.ohms_exp == -2:
                return "0.0" + rendered_num
            if self.ohms_exp == -3:
                return "0.00" + rendered_num

        return self.get_prefixed_number() + " " + self.get_prefix() + "\u2126"

    def resistor_color_table(self, num: int) -> HexColor:
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

    def draw_fancy_resistor_stripe(
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

    def draw_resistor_stripe_border(self, c: Canvas, x: float, y: float, width: float, height: float) -> None:
        c.setLineWidth(0.3)
        c.setFillColor(black, 0.0)
        c.setStrokeColorRGB(0.2, 0.2, 0.2, 0.5)
        c.rect(x, y, width, height, fill=0, stroke=1)

    def draw_resistor_stripe(self, c: Canvas, x: float, y: float, width: float, height: float, stripe_value: int) -> None:
        if 0 <= stripe_value <= 9:
            c.setFillColor(self.resistor_color_table(stripe_value))
            c.rect(x, y, width, height, fill=1, stroke=0)
            self.draw_resistor_stripe_border(c, x, y, width, height)
            return

        elif stripe_value == -1:
            gold_table = [
                HexColor("#FFF0A0"),
                HexColor("#FFE55C"),
                HexColor("#FFD700"),
                HexColor("#D1B000"),
            ]

            self.draw_fancy_resistor_stripe(c, x, y, width, height, gold_table)
            self.draw_resistor_stripe_border(c, x, y, width, height)
            return
        elif stripe_value == -2:
            silver_table = [
                HexColor("#D0D0D0"),
                HexColor("#A9A9A9"),
                HexColor("#929292"),
                HexColor("#7B7B7B"),
            ]

            self.draw_fancy_resistor_stripe(c, x, y, width, height, silver_table)
            self.draw_resistor_stripe_border(c, x, y, width, height)
            return
        else:
            c.setLineWidth(0.5)
            c.setFillColor(gray, 0.3)
            c.setStrokeColorRGB(0.5, 0.5, 0.5, 1.0)
            c.rect(x, y, width, height, fill=1, stroke=1)
            c.line(x, y, x + width, y + height)
            c.line(x + width, y, x, y + height)
            return

    def draw_resistor_colorcode(
            self,
            c: Canvas,
            color1: object,
            color2: object,
            x: float,
            y: float,
            width: float,
            height: float,
            num_codes: int,
    ) -> None:

        if self.ohms_exp < num_codes - 4:
            return

        border=0
        corner=0
        width_without_corner=width
        stripe_width=width/num_codes/2

        if self.ohms_val == 0:
            self.draw_resistor_stripe(c,
                                 x + border + corner + stripe_width / 2 + 2 * stripe_width * 2,
                                 y + border,
                                 stripe_width,
                                 height - 2 * border,
                                 0)
        else:
            for i in range(num_codes):
                if i == num_codes - 1:
                    stripe_value = self.ohms_exp + 2 - num_codes
                else:
                    stripe_value = self.ohms_val
                    for _ in range(2-i):
                        stripe_value //= 10
                    stripe_value %= 10

                self.draw_resistor_stripe(c,
                                     x + border + corner + stripe_width / 2 + 2 * stripe_width * i,
                                     y + border,
                                     stripe_width,
                                     height - 2 * border,
                                     stripe_value)

        c.setFillColor(black)
        c.setStrokeColor(black, 1)
        c.setLineWidth(0.5)

    def get_3digit_code(self) -> str:
        if self.ohms_val % 10 != 0:
            return ""

        if self.ohms_val == 0:
            return "000"

        digits = str(self.ohms_val // 10)

        if self.ohms_exp > 0:
            multiplier = str(self.ohms_exp - 1)
            return digits + multiplier

        if self.ohms_exp == 0:
            return digits[0] + "R" + digits[1]

        if self.ohms_exp == -1:
            return "R" + digits

        if self.ohms_exp == -2:
            if self.ohms_val % 100 != 0:
                return ""
            return "R0" + digits[0]

        return ""

    def get_4digit_code(self) -> str:
        digits = str(self.ohms_val)

        if self.ohms_val == 0:
            return "0000"

        if self.ohms_exp > 1:
            multiplier = str(self.ohms_exp - 2)
            return digits + multiplier

        if self.ohms_exp == 1:
            return digits[0] + digits[1] + "R" + digits[2]

        if self.ohms_exp == 0:
            return digits[0] + "R" + digits[1] + digits[2]

        if self.ohms_exp == -1:
            return "R" + digits

        if self.ohms_exp == -2:
            if self.ohms_val % 10 != 0:
                return ""
            return "R0" + digits[0] + digits[1]

        if self.ohms_exp == -3:
            if self.ohms_val % 100 != 0:
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

        if self.ohms_val not in eia98_coding_table:
            return ""

        digits = eia98_coding_table[self.ohms_val]

        multiplier_table = ["Z", "Y", "X", "A", "B", "C", "D", "E", "F"]
        if not (0 <= self.ohms_exp+1 < len(multiplier_table)):
            return ""

        multiplier = multiplier_table[self.ohms_exp+1]

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
        space_between = 5

        value_string = self.format_value()
        value_width = c.stringWidth(value_string, 'Arial Bold', value_font_size * 1.35)

        text_middle = rect.left + rect.width/2
        text_bottom = rect.bottom + rect.height/4 - value_font_size/5
        c.setFont('Arial Bold', value_font_size * 1)
        c.drawCentredString(text_middle, text_bottom, value_string)
        c.drawCentredString(text_middle, text_bottom+rect.height/2, value_string)

    
        # Draw resistor color code
        for bottom in (rect.bottom+rect.height/16, rect.bottom+rect.height*8/16):
            for stripes in (3,4):
                self.draw_resistor_colorcode(c,
                                        toColor("hsl(55, 54%, 100%)"), toColor("hsl(55, 54%, 70%)"),
                                        rect.left+rect.width*((stripes-3)*2/3),
                                        bottom,
                                        rect.width/3, rect.height*7/16,
                                        stripes)

        c.setFont('Arial Bold', smd_font_size * 1.35)
        for i in (0,rect.height/2):
            c.drawString(rect.left + rect.width/3, rect.bottom +
                        rect.height/13+i, self.get_3digit_code())
            c.drawCentredString(rect.left + rect.width/2, rect.bottom +
                                rect.height/13+i, self.get_4digit_code())
            c.drawRightString(rect.left + rect.width*2/3, rect.bottom +
                            rect.height/13+i, self.get_eia98_code())


def begin_page(c: Canvas, layout: PaperConfig, draw_outlines: bool) -> None:
    # Draw the outlines of the stickers. Not recommended for the actual print.
    if draw_outlines:
        render_outlines(c, layout)


def end_page(c: Canvas) -> None:
    c.showPage()


def render_stickers(
    c: Canvas,
    layout: PaperConfig,
    values: List[Component],
    draw_outlines: bool,
    draw_center_line: bool,
) -> None:
    # Set the title
    c.setTitle(f"Resistor Labels - {layout.paper_name}")

    # Begin the first page
    begin_page(c, layout, draw_outlines)

    for (position, value) in enumerate(values):
        rowId = (position // layout.num_stickers_horizontal) % layout.num_stickers_vertical
        columnId = position % layout.num_stickers_horizontal

        # If we are at the first sticker of a new page, change the page
        if rowId == 0 and columnId == 0 and position != 0:
            end_page(c)
            begin_page(c, layout, draw_outlines)

        if value is not None:
            with StickerRect(c, layout, rowId, columnId, False) as rect:
                value.draw(c, rect, draw_center_line)

    # End the page one final time
    end_page(c)


def render_outlines(c: Canvas, layout: PaperConfig) -> None:
    for row in range(layout.num_stickers_vertical):
        for column in range(layout.num_stickers_horizontal):
            with StickerRect(c, layout, row, column, False) as rect:
                c.setStrokeColor(black, 0.1)
                c.setLineWidth(0)
                c.roundRect(rect.left, rect.bottom, rect.width, rect.height, rect.corner)


def main() -> None:

    # ############################################################################
    # Select the correct type of paper you want to print on.
    # ############################################################################
    layout = VYSOCINA
    # layout = AVERY_L7157
    # layout = EJ_RANGE_24

    # ############################################################################
    # Put your own component values in here!
    #
    # Add "None" if no label should get generated at a specific position.
    # ############################################################################

    components: List[Component] = []

    common_resistor_values: List[float] = [
        1, 1.2, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    ]

    for exponent in range(6):
        for value in common_resistor_values:
            components.append(Resistor(value * (10 ** exponent)))

    # ############################################################################
    # Further configuration options
    #
    # Change the following options as you desire.
    # ############################################################################

    # Draws the line where the stickers should be folded.
    # Disable this if you don't like the line.
    draw_center_line = True

    # Draw the outlines of the stickers.
    # This is primarily a debugging option and should most likely not be enabled
    # for the actual printing.
    draw_outlines = False

    # ############################################################################
    # PDF generation
    #
    # The following is the actual functionality of this script - to generate
    # the ResistorLabels PDF file.
    # ############################################################################

    # Create the render canvas
    c = Canvas("ResistorLabels.pdf", pagesize=layout.pagesize)

    # Render the stickers
    render_stickers(c, layout, components, draw_outlines, draw_center_line)

    # Store canvas to PDF file
    c.save()


if __name__ == "__main__":
    main()
