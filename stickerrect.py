from reportlab.pdfgen.canvas import Canvas

from paperconfig import PaperConfig

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


