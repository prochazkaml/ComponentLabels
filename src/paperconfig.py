from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.units import inch, mm
from typing import Tuple

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



