import pytest
from src.piece import Piece

def test_piece_initialization():
    shape = [(0, 0), (1, 0)]
    color = (255, 0, 0)
    piece = Piece(shape, color)
    
    assert piece.shape == shape
    assert piece.color == color
    assert piece.is_dragging is False

def test_get_cells():
    shape = [(0, 0), (0, 1)]
    piece = Piece(shape, (255, 255, 255))
    cells = piece.get_cells(base_x=2, base_y=3)
    
    assert cells == [(2, 3), (2, 4)]