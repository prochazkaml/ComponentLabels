from reportlab.pdfgen.canvas import Canvas

from src.stickerrect import StickerRect

class Component:
    def draw(self, c: Canvas, rect: StickerRect, draw_center_line: bool) -> None:
        raise Exception("called parent class")

    def get_value(self) -> float:
        return self.val * math.pow(10, self.exp - 2)

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

