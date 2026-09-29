"""Grid class managing the 8x8 matrix state and clear operations."""

from src.config import GRID_SIZE

class Grid:
    def __init__(self):
        self.matrix = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def can_place(self, piece, grid_x, grid_y):
        for dx, dy in piece.shape:
            gx = grid_x + dx
            gy = grid_y + dy
            if not (0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE):
                return False
            if self.matrix[gy][gx] != 0:
                return False
        return True

    def place_piece(self, piece, grid_x, grid_y):
        for dx, dy in piece.shape:
            gx = grid_x + dx
            gy = grid_y + dy
            self.matrix[gy][gx] = piece.color

    def clear_full_lines(self):
        rows_to_clear = [r for r in range(GRID_SIZE) if all(self.matrix[r][c] != 0 for c in range(GRID_SIZE))]
        cols_to_clear = [c for c in range(GRID_SIZE) if all(self.matrix[r][c] != 0 for r in range(GRID_SIZE))]

        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                self.matrix[r][c] = 0

        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                self.matrix[r][c] = 0

        return len(rows_to_clear) + len(cols_to_clear)