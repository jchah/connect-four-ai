"""
connect_four_logic.py
Pure Connect‑Four game engine – no GUI, just rules.

Usage example
-------------
from connect_four_logic import ConnectFour

game = ConnectFour()

# drop a piece for the current player in column 3 (0‑based)
row, col = game.drop_piece(3)

# inspect the board
print(game.board)

# check the game state
if game.game_over:
    if game.winner:
        print(f"Player {game.winner} wins!")
    else:
        print("It’s a draw!")
"""

from __future__ import annotations

import numpy as np


class ConnectFour:
    """Reusable Connect‑Four rules engine (6 × 7 grid, 4 in a row to win)."""

    ROWS: int = 6
    COLS: int = 7
    CONNECT: int = 4

    EMPTY: int = 0
    PLAYER1: int = 1
    PLAYER2: int = 2

    def __init__(self) -> None:
        self.winner = None
        self.game_over = None
        self.moves_made = None
        self.current_player = None
        self._next_row = None
        self.board = None
        self.reset()

    # --------------------------------------------------------------------- #
    #  Public API                                                           #
    # --------------------------------------------------------------------- #

    def reset(self) -> None:
        """Start a fresh game."""
        self.board: np.ndarray = np.zeros((self.ROWS, self.COLS), dtype=int)
        # index of the next empty row in each column (‑1 means column full)
        self._next_row: dict[int, int] = {c: self.ROWS - 1 for c in range(self.COLS)}
        self.current_player: int = self.PLAYER1
        self.moves_made: int = 0
        self.game_over: bool = False
        self.winner: int | None = None  # 1, 2 or None for draw/in‑progress

    def drop_piece(self, col: int) -> tuple[int, int]:
        """
        Drop a piece for the current player into *col* (0‑based).

        Returns the (row, col) where the disc landed.
        Raises ValueError for illegal columns or full columns.
        Raises RuntimeError if the game has already finished.
        """
        if self.game_over:
            raise RuntimeError("The game is already finished.")

        if not 0 <= col < self.COLS:
            raise ValueError(f"Column must be between 0 and {self.COLS - 1}.")

        row: int = self._next_row[col]
        if row < 0:
            raise ValueError("That column is full.")

        # place the disc
        self.board[row, col] = self.current_player
        self._next_row[col] -= 1
        self.moves_made += 1

        # check for a winning move
        if self._is_winning_move(row, col):
            self.game_over = True
            self.winner = self.current_player
        elif self.moves_made == self.ROWS * self.COLS:
            self.game_over = True  # draw
        else:
            # swap turns
            self.current_player = (
                self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
            )

        return row, col

    # --------------------------------------------------------------------- #
    #  Internals                                                            #
    # --------------------------------------------------------------------- #

    def _is_winning_move(self, row: int, col: int) -> bool:
        """True if dropping at (row, col) finished the game."""
        piece: int = self.board[row, col]

        # direction vectors: horizontal, vertical, two diagonals
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            if self._count_consecutive(row, col, dr, dc, piece) >= self.CONNECT:
                return True
        return False

    def _count_consecutive(
        self, row: int, col: int, dr: int, dc: int, piece: int
    ) -> int:
        """
        Count contiguous *piece* discs through (row, col) in both directions
        given by (dr, dc). Example: dr=1, dc=‑1 walks ↘ and ↖.
        """
        count: int = 1  # include the drop point itself

        # forward direction
        r, c = row + dr, col + dc
        while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r, c] == piece:
            count += 1
            r += dr
            c += dc

        # reverse direction
        r, c = row - dr, col - dc
        while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r, c] == piece:
            count += 1
            r -= dr
            c -= dc

        return count

    # --------------------------------------------------------------------- #
    #  Convenience                                                          #
    # --------------------------------------------------------------------- #

    @property
    def is_draw(self) -> bool:
        """True if the game ended without a winner."""
        return self.game_over and self.winner is None

    def __str__(self) -> str:  # nice print‑out for debugging
        return np.array_str(self.board)

    # Allow indexing like engine[row, col] if you really want it
    def __getitem__(self, idx):
        return self.board[idx]
