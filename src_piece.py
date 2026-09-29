"""Piece class representing interactive block components."""

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.spawn_pos = (0, 0)
        self.pos = [0, 0]
        self.is_dragging = False

    def get_cells(self, base_x=None, base_y=None):
        if base_x is None or base_y is None:
            base_x, base_y = self.pos[0], self.pos[1]
        return [(base_x + dx, base_y + dy) for dx, dy in self.shape]