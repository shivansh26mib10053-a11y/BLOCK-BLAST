# Problem Statement: Block Blast Pygame Implementation

## 1. Objective
Design and develop a 2D grid-based puzzle game inspired by popular block-placement games such as *Block Blast!*. The core goal is to maximize the score by strategic placement of geometric block shapes onto a fixed $8 \times 8$ grid to complete and clear rows and columns.

## 2. Requirements & Specifications
- **Grid Environment:** A standard $8 \times 8$ matrix representation of cells.
- **Piece Generation:**
  - Provide a variety of shapes (1x1, 1x2, 1x3, 2x2, L-shapes, 3x3 squares).
  - Spawn 3 random pieces per round.
  - Refresh the piece pool once all 3 pieces are successfully positioned on the grid.
- **Player Interaction:** Smooth mouse-based drag-and-drop mechanics to position pieces on the board.
- **Clearing Mechanics:**
  - Complete horizontal rows or vertical columns must be detected instantly and cleared.
  - Support multi-line combo scoring.
- **Game Termination:**
  - Continuous evaluation of available grid space after every move.
  - If none of the remaining pieces fit on the board, trigger a Game Over state with an option to reset.