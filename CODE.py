import pygame
import random
import sys

# --- Constants & Configuration ---
GRID_SIZE = 8
CELL_SIZE = 50
GRID_MARGIN = 4
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 100

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700

# Color Palette (Hex)
COLOR_BG = (22, 27, 34)
COLOR_GRID_BG = (13, 17, 23)
COLOR_EMPTY = (33, 38, 45)
COLOR_TEXT = (240, 246, 252)

# Block Colors
PIECE_COLORS = [
    (255, 107, 107),  # Red
    (78, 205, 196),   # Teal
    (255, 230, 109),  # Yellow
    (26, 83, 92),     # Dark Green
    (247, 255, 247),  # White-ish
    (255, 159, 243),  # Pink
    (84, 160, 255),   # Blue
]

# Block Shapes (Represented as relative coordinates (x, y))
SHAPES = [
    # 1x1 Single Dot
    [(0, 0)],
    # 1x2 and 2x1 Bars
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    # 1x3 and 3x1 Bars
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2)],
    # 1x4 and 4x1 Bars
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    # 2x2 Square
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    # 3x3 Square
    [(x, y) for x in range(3) for y in range(3)],
    # L-Shapes
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(2, 0), (0, 1), (1, 1), (2, 1)],
]


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


class BlockBlastGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Block Blast Pygame")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 48, bold=True)

        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.spawn_pieces()

    def spawn_pieces(self):
        self.pieces = []
        spawn_y = 540
        spacing = WINDOW_WIDTH // 4

        for i in range(3):
            shape = random.choice(SHAPES)
            color = random.choice(PIECE_COLORS)
            piece = Piece(shape, color)

            # Center piece relative to its spawn area
            spawn_x = spacing * (i + 1) - CELL_SIZE
            piece.spawn_pos = (spawn_x, spawn_y)
            piece.pos = [spawn_x, spawn_y]
            self.pieces.append(piece)

    def draw_board(self):
        # Background container for the grid
        grid_width = GRID_SIZE * CELL_SIZE
        pygame.draw.rect(
            self.screen,
            COLOR_GRID_BG,
            (BOARD_OFFSET_X - 6, BOARD_OFFSET_Y - 6, grid_width + 12, grid_width + 12),
            border_radius=10,
        )

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = BOARD_OFFSET_X + col * CELL_SIZE
                y = BOARD_OFFSET_Y + row * CELL_SIZE
                color = self.grid[row][col] if self.grid[row][col] != 0 else COLOR_EMPTY
                
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x + GRID_MARGIN // 2, y + GRID_MARGIN // 2, CELL_SIZE - GRID_MARGIN, CELL_SIZE - GRID_MARGIN),
                    border_radius=6,
                )

    def draw_piece(self, piece, scale=1.0):
        for dx, dy in piece.shape:
            x = piece.pos[0] + dx * CELL_SIZE * scale
            y = piece.pos[1] + dy * CELL_SIZE * scale
            size = (CELL_SIZE - GRID_MARGIN) * scale

            pygame.draw.rect(
                self.screen,
                piece.color,
                (x, y, size, size),
                border_radius=int(6 * scale),
            )

    def screen_to_grid(self, x, y):
        grid_x = round((x - BOARD_OFFSET_X) / CELL_SIZE)
        grid_y = round((y - BOARD_OFFSET_Y) / CELL_SIZE)
        return grid_x, grid_y

    def can_place(self, piece, grid_x, grid_y):
        for dx, dy in piece.shape:
            gx = grid_x + dx
            gy = grid_y + dy
            if not (0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE):
                return False
            if self.grid[gy][gx] != 0:
                return False
        return True

    def place_piece(self, piece, grid_x, grid_y):
        for dx, dy in piece.shape:
            gx = grid_x + dx
            gy = grid_y + dy
            self.grid[gy][gx] = piece.color

        self.score += len(piece.shape) * 10
        self.pieces.remove(piece)
        self.clear_lines()

        # If all 3 pieces are used, spawn a new set
        if not self.pieces:
            self.spawn_pieces()

        # Check for game over
        if not self.check_any_moves_left():
            self.game_over = True

    def clear_lines(self):
        rows_to_clear = [r for r in range(GRID_SIZE) if all(self.grid[r][c] != 0 for c in range(GRID_SIZE))]
        cols_to_clear = [c for c in range(GRID_SIZE) if all(self.grid[r][c] != 0 for r in range(GRID_SIZE))]

        lines_cleared = len(rows_to_clear) + len(cols_to_clear)

        for r in rows_to_clear:
            for c in range(GRID_SIZE):
                self.grid[r][c] = 0

        for c in cols_to_clear:
            for r in range(GRID_SIZE):
                self.grid[r][c] = 0

        # Combo scoring bonus
        if lines_cleared > 0:
            self.score += (lines_cleared * 100) * lines_cleared

    def check_any_moves_left(self):
        for piece in self.pieces:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.can_place(piece, c, r):
                        return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

            if self.game_over:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for piece in self.pieces:
                    # Simple hitbox check around the piece origin
                    px, py = piece.pos
                    if px <= mx <= px + 100 and py <= my <= py + 100:
                        piece.is_dragging = True
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for piece in self.pieces:
                    if piece.is_dragging:
                        piece.is_dragging = False
                        grid_x, grid_y = self.screen_to_grid(piece.pos[0], piece.pos[1])
                        if self.can_place(piece, grid_x, grid_y):
                            self.place_piece(piece, grid_x, grid_y)
                        else:
                            # Snap back if invalid placement
                            piece.pos = list(piece.spawn_pos)

            elif event.type == pygame.MOUSEMOTION:
                for piece in self.pieces:
                    if piece.is_dragging:
                        # Offset so cursor is near center of the block
                        piece.pos[0] = event.pos[0] - 25
                        piece.pos[1] = event.pos[1] - 25

    def draw_ui(self):
        # Draw Score
        score_surf = self.font.render(f"SCORE: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_surf, (BOARD_OFFSET_X, 40))

        # Game Over Screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            go_surf = self.large_font.render("GAME OVER", True, (255, 85, 85))
            rect = go_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(go_surf, rect)

            restart_surf = self.font.render("Press 'R' to Restart", True, COLOR_TEXT)
            rect_r = restart_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(restart_surf, rect_r)

    def run(self):
        while True:
            self.screen.fill(COLOR_BG)
            self.handle_events()
            self.draw_board()

            # Render available pieces at the bottom
            for piece in self.pieces:
                scale = 1.0 if piece.is_dragging else 0.6
                self.draw_piece(piece, scale=scale)

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    game = BlockBlastGame()
    game.run()