from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.components.component import Component
from src.components.resistor import Resistor
from src.components.capacitor import Capacitor
from src.components.transistor import NPNBJT, PNPBJT, NMOSFET, PMOSFET
from src.components.diode import Diode, SchottkyDiode, ZenerDiode, LED
from src.components.nut import SquareNut, HexNut
from src.components.screw import RecessedHeadScrew, RoundHeadScrew
from src.components.threadedinsert import ThreadedInsert
from src.components.spring import CompressionSpring, ExtensionSpring
from src.paperconfig import PaperConfig, AVERY_5260, AVERY_L7157, VYSOCINA
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

    for exponent in range(6): # Ohms to 100kOhms (exclusive)
        for value in common_resistor_values:
            components.append(Resistor(value * (10 ** exponent)))

    resistor_values: List[float] = [
        3300000, 4700000, 5600000, 10000000
    ]
    
    for value in resistor_values:
        components.append(Resistor(value))

    capacitor_values: List[float] = [ # in pF
        2, 2.2, 3, 5, 10, 15, 22, 30, 33, 47, 68, 75, 82, 100, 150, 220, 330, 470, 680,
        1000, 1500, 2200, 3300, 4700, 6800, 10000, 15000, 33000, 47000, 68000, 100000
    ]

    for value in capacitor_values:
        components.append(Capacitor(value * .000000000001))

    components.append(RoundHeadScrew("M5", "10 mm", "4.2 mm", "30 mm"))
    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "6 mm"))
    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "16 mm"))
    components.append(RoundHeadScrew("M3", "6 mm", "2.6 mm", "20 mm"))

    components.append(RecessedHeadScrew("M3", "5.6 mm", "2 mm", "7 mm"))
    
    components.append(HexNut("M5", "4 mm", "8 mm", "9 mm"))
    components.append(HexNut("M3", "2.2 mm", "5.5 mm", "6.3 mm"))

    components.append(SquareNut("M5", "3 mm", "8 mm", "11.3 mm"))
    
    components.append(ThreadedInsert("M2", "3.5 mm", "3 mm"))
    components.append(ThreadedInsert("M2", "3.5 mm", "4 mm"))
    components.append(ThreadedInsert("M2", "3.5 mm", "5 mm"))
    components.append(ThreadedInsert("M2.5", "3.5 mm", "3 mm"))
    components.append(ThreadedInsert("M2.5", "3.5 mm", "4 mm"))
    components.append(ThreadedInsert("M2.5", "3.5 mm", "5 mm"))
    components.append(ThreadedInsert("M3", "4.5 mm", "3 mm"))
    components.append(ThreadedInsert("M3", "4.5 mm", "4 mm"))
    components.append(ThreadedInsert("M3", "5 mm", "4 mm"))
    components.append(ThreadedInsert("M3", "5 mm", "5 mm"))

    components.append(ExtensionSpring("5 mm", "20.5 mm"))
    components.append(ExtensionSpring("5.5 mm", "25.5 mm"))
    components.append(ExtensionSpring("6.5 mm", "22 mm"))
    components.append(ExtensionSpring("8.5 mm", "47 mm"))
    components.append(ExtensionSpring("7 mm", "51 mm"))
    components.append(ExtensionSpring("7 mm", "38 mm"))
    components.append(ExtensionSpring("8.5 mm", "36.5 mm"))
    components.append(ExtensionSpring("8 mm", "28.5 mm"))
    components.append(ExtensionSpring("8 mm", "31.5 mm"))
    components.append(ExtensionSpring("8 mm", "44.5 mm"))
    components.append(ExtensionSpring("4 mm", "79.5 mm"))
    components.append(ExtensionSpring("4.5 mm", "44.5 mm"))

    components.append(CompressionSpring("7 mm", "12.5 mm"))
    components.append(CompressionSpring("6.5 mm", "10 mm"))
    components.append(CompressionSpring("7 mm", "19 mm"))
    components.append(CompressionSpring("5.5 mm", "38 mm"))
    components.append(CompressionSpring("9.5 mm", "16 mm"))
    components.append(CompressionSpring("9.5 mm", "19 mm"))
    components.append(CompressionSpring("9 mm", "35 mm"))
    components.append(CompressionSpring("5.5 mm", "17 mm"))

    components.append(NPNBJT("2N2222", 3, 2, 1, "0.6 (6) V", "600 mA", "40 V"))
    components.append(NPNBJT("2N3904", 3, 2, 1, "0.65 (6) V", "200 mA", "40 V"))
    components.append(PNPBJT("2N3906", 3, 2, 1, "-0.65 (-5) V", "-200 mA", "-40 V"))
    components.append(PNPBJT("2N5401", 3, 2, 1, "-1 (-5) V", "-600 mA", "-150 V"))
    components.append(NPNBJT("2N5551", 3, 2, 1, "1 (6) V", "600 mA", "160 V"))
    components.append(PNPBJT("A1015", 2, 3, 1, "-1.1 (-5) V", "-150 mA", "-50 V"))
    components.append(NPNBJT("C1815", 2, 3, 1, "1 (5) V", "150 mA", "50 V"))
    components.append(NPNBJT("C945", 2, 3, 1, "1 (5) V", "150 mA", "50 V"))
    
    components.append(NPNBJT("S8050", 3, 2, 1, "1 (6) V", "1.5 A", "25 V"))
    components.append(PNPBJT("S8550", 3, 2, 1, "-0.66 (-6) V", "-1.5 A", "-25 V"))
    components.append(PNPBJT("S9012", 3, 2, 1, "-0.66 (-5) V", "-500 mA", "-20 V"))
    components.append(NPNBJT("S9013", 3, 2, 1, "1.2 (5) V", "500 mA", "25 V"))
    components.append(NPNBJT("S9014", 3, 2, 1, "0.85 (5) V", "500 mA", "45 V"))
    components.append(PNPBJT("S9015", 3, 2, 1, "-1 (-5) V", "-100 mA", "-45 V"))
    components.append(PNPBJT("BC327", 1, 2, 3, "-1.2 (-5) V", "-800 mA", "-45 V"))
    components.append(NPNBJT("BC337", 1, 2, 3, "1.2 (5) V", "800 mA", "45 V"))
    
    components.append(NPNBJT("BC517", 1, 2, 3, "1.4 (10) V", "1.2 A", "30 V"))
    components.append(NPNBJT("BC547", 1, 2, 3, "0.9 (6) V", "100 mA", "45 V"))
    components.append(NPNBJT("BC548", 1, 2, 3, "0.9 (5) V", "100 mA", "30 V"))
    components.append(NPNBJT("BC549", 1, 2, 3, "0.9 (5) V", "100 mA", "30 V"))
    components.append(NPNBJT("BC550", 1, 2, 3, "0.9 (5) V", "100 mA", "45 V"))
    components.append(PNPBJT("BC556", 1, 2, 3, "-1 (-5) V", "-100 mA", "-65 V"))
    components.append(PNPBJT("BC557", 1, 2, 3, "-1 (-5) V", "-100 mA", "-45 V"))
    components.append(PNPBJT("BC588", 1, 2, 3, "-1 (-5) V", "-100 mA", "-30 V"))
    
    components.append(NMOSFET("IRF520", 1, 2, 3, "2..4 V", "6.5 A", "100 V"))
    components.append(PMOSFET("IRF9520", 1, 2, 3, "-2..4 V", "-4.8 A", "-100 V"))
    
    components.append(Diode("1N4148", "1 V", "300 mA", "75 V"))
    components.append(Diode("1N4007", "1.1 V", "1 A", "1 kV"))
    components.append(SchottkyDiode("PMEG3050", "360 mV", "5 A", "30 V"))
    components.append(ZenerDiode("ZPD3V6", "3.4-3.8 V", "5 mA", "1 V"))

    components.append(LED("5 mm", "1.2 V", "20 mA", "940 nm", HexColor("#800000")))
    components.append(LED("5 mm", "3.0-3.2 V", "20 mA", "* nm", HexColor("#FFFFFF")))
    components.append(LED("5 mm", "1.9-2.1 V", "20 mA", "620-625 nm", HexColor("#FF0000")))
    components.append(LED("5 mm", "1.9-2.1 V", "20 mA", "588-590 nm", HexColor("#FFFF00")))
    components.append(LED("5 mm", "2.1-3.0 V", "20 mA", "567-570 nm", HexColor("#00FF00")))
    components.append(LED("5 mm", "3.0-3.2 V", "20 mA", "455-465 nm", HexColor("#0000FF")))

    components.append(LED("3 mm", "3.0-3.2 V", "20 mA", "* nm", HexColor("#FFFFFF")))
    components.append(LED("3 mm", "1.9-2.1 V", "20 mA", "620-625 nm", HexColor("#FF0000")))
    components.append(LED("3 mm", "1.9-2.1 V", "20 mA", "588-590 nm", HexColor("#FFFF00")))
    components.append(LED("3 mm", "2.1-3.0 V", "20 mA", "567-570 nm", HexColor("#00FF00")))
    components.append(LED("3 mm", "3.0-3.2 V", "20 mA", "455-465 nm", HexColor("#0000FF")))
    
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

