import pytest
from src.grid import Grid
from src.piece import Piece
from src.config import GRID_SIZE

def test_grid_initialization():
    grid = Grid()
    assert len(grid.matrix) == GRID_SIZE
    assert len(grid.matrix[0]) == GRID_SIZE

def test_can_place_valid():
    grid = Grid()
    piece = Piece([(0, 0), (1, 0)], (255, 0, 0))
    assert grid.can_place(piece, 0, 0) is True

def test_can_place_out_of_bounds():
    grid = Grid()
    piece = Piece([(0, 0), (1, 0)], (255, 0, 0))
    assert grid.can_place(piece, GRID_SIZE - 1, 0) is False

def test_clear_full_line():
    grid = Grid()
    # Fill row index 0 manually
    for c in range(GRID_SIZE):
        grid.matrix[0][c] = (255, 255, 255)
    
    cleared = grid.clear_full_lines()
    assert cleared == 1
    assert all(grid.matrix[0][c] == 0 for c in range(GRID_SIZE))