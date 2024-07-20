from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.components.component import Component
from src.components.resistor import Resistor
from src.components.capacitor import Capacitor
from src.components.nut import SquareNut, HexNut
from src.components.screw import RecessedHeadScrew, RoundHeadScrew
from src.components.transistor import NPNBJT, PNPBJT, NMOSFET, PMOSFET
from src.paperconfig import PaperConfig, VYSOCINA
from src.stickerrect import StickerRect

from typing import List

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
    pdfmetrics.registerFont(TTFont('main', 'Roboto-Bold.ttf'))

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
        # E6
        # 1, 1.5, 2.2, 3.3, 4.7, 6.8

        # E12
        # 1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2

        # Mostly complete E24. The bundle of resistors I bought did not come with some.
        1, 1.2, 1.5, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1

        # E24
        # 1, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2, 2.2, 2.4, 2.7, 3, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    ]

    # for exponent in range(6): # Ohms to 100kOhms (exclusive)
    #     for value in common_resistor_values:
    #         components.append(Resistor(value * (10 ** exponent)))

    # resistor_values: List[float] = [
    #     3300000, 4700000, 5600000, 10000000
    # ]
    #
    # for value in resistor_values:
    #     components.append(Resistor(value))

    # capacitor_values: List[float] = [ # in pF
    #     2, 2.2, 3, 5, 10, 15, 22, 30, 33, 47, 68, 75, 82, 100, 150, 220, 330, 470, 680,
    #     1000, 1500, 2200, 3300, 4700, 6800, 10000, 15000, 33000, 47000, 68000, 100000
    # ]

    capacitor_values: List[float] = [ # in pF
        2.2
    ]

    for value in capacitor_values:
        components.append(Capacitor(value * .000000000001))

    components.append(HexNut("test", 2.4, 5.5, 6.5))
    components.append(SquareNut("test", 2.4, 5.5, 6.5))
    components.append(RoundHeadScrew("test", 2.4, 5.5, 6.5))
    components.append(RecessedHeadScrew("test", 2.4, 5.5, 6.5))
    components.append(NPNBJT("test", 1, 2, 3, 4, 5, 6))
    components.append(PNPBJT("test", 1, 2, 3, 4, 5, 6))
    components.append(NMOSFET("test", 1, 2, 3, 4, 5, 6))
    components.append(PMOSFET("test", 1, 2, 3, 4, 5, 6))

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
    # the ComponentLabels PDF file.
    # ############################################################################

    # Create the render canvas
    c = Canvas("ComponentLabels.pdf", pagesize=layout.pagesize)

    # Render the stickers
    render_stickers(c, layout, components, draw_outlines, draw_center_line)

    # Store canvas to PDF file
    c.save()

