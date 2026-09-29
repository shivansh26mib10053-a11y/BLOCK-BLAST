"""Global constants and configurations for Block Blast."""

GRID_SIZE = 8
CELL_SIZE = 50
GRID_MARGIN = 4
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 100

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700

# Color Palette (RGB)
COLOR_BG = (22, 27, 34)
COLOR_GRID_BG = (13, 17, 23)
COLOR_EMPTY = (33, 38, 45)
COLOR_TEXT = (240, 246, 252)

PIECE_COLORS = [
    (255, 107, 107),  # Red
    (78, 205, 196),   # Teal
    (255, 230, 109),  # Yellow
    (26, 83, 92),     # Dark Green
    (247, 255, 247),  # Light Mint
    (255, 159, 243),  # Pink
    (84, 160, 255),   # Blue
]

SHAPES = [
    [(0, 0)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(x, y) for x in range(3) for y in range(3)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(2, 0), (0, 1), (1, 1), (2, 1)],
]