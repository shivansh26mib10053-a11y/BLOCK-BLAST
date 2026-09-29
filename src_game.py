"""Core Pygame engine controller for Block Blast."""

import random
import sys
import pygame
from src.config import (
    BOARD_OFFSET_X, BOARD_OFFSET_Y, CELL_SIZE, COLOR_BG, COLOR_EMPTY,
    COLOR_GRID_BG, COLOR_TEXT, GRID_MARGIN, GRID_SIZE, PIECE_COLORS,
    SHAPES, WINDOW_HEIGHT, WINDOW_WIDTH
)
from src.grid import Grid
from src.piece import Piece


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
        self.grid = Grid()
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

            spawn_x = spacing * (i + 1) - CELL_SIZE
            piece.spawn_pos = (spawn_x, spawn_y)
            piece.pos = [spawn_x, spawn_y]
            self.pieces.append(piece)

    def draw_board(self):
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
                color = self.grid.matrix[row][col] if self.grid.matrix[row][col] != 0 else COLOR_EMPTY
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

    def check_any_moves_left(self):
        for piece in self.pieces:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if self.grid.can_place(piece, c, r):
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
                    px, py = piece.pos
                    if px <= mx <= px + 100 and py <= my <= py + 100:
                        piece.is_dragging = True
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for piece in self.pieces:
                    if piece.is_dragging:
                        piece.is_dragging = False
                        grid_x, grid_y = self.screen_to_grid(piece.pos[0], piece.pos[1])
                        if self.grid.can_place(piece, grid_x, grid_y):
                            self.grid.place_piece(piece, grid_x, grid_y)
                            self.score += len(piece.shape) * 10
                            lines = self.grid.clear_full_lines()
                            if lines > 0:
                                self.score += (lines * 100) * lines
                            self.pieces.remove(piece)

                            if not self.pieces:
                                self.spawn_pieces()

                            if not self.check_any_moves_left():
                                self.game_over = True
                        else:
                            piece.pos = list(piece.spawn_pos)

            elif event.type == pygame.MOUSEMOTION:
                for piece in self.pieces:
                    if piece.is_dragging:
                        piece.pos[0] = event.pos[0] - 25
                        piece.pos[1] = event.pos[1] - 25

    def draw_ui(self):
        score_surf = self.font.render(f"SCORE: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_surf, (BOARD_OFFSET_X, 40))

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

            for piece in self.pieces:
                scale = 1.0 if piece.is_dragging else 0.6
                self.draw_piece(piece, scale=scale)

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)