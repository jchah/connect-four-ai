# connect_four_gui.py
# -------------------
# Tkinter front‑end for the reusable engine in connect_four_logic.py

import tkinter as tk

from connect_four_logic import ConnectFour

# ──────────────────────────────────────────────────────────────────────
#  GUI constants
# ──────────────────────────────────────────────────────────────────────
CELL_SIZE      = 80      # pixels
DISC_OUTLINE   = 2
COLOR_BG       = "#0a4ea1"   # board background (blue)
COLOR_EMPTY    = "white"
COLOR_P1       = "#f5d20c"   # yellow
COLOR_P2       = "#d62828"   # red


class ConnectFourGUI:
    """Simple Tk‑inter wrapper around the pure Connect Four engine."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Connect Four")

        # rules engine --------------------------------------------------
        self.engine = ConnectFour()

        # canvas --------------------------------------------------------
        width  = ConnectFour.COLS * CELL_SIZE
        height = ConnectFour.ROWS * CELL_SIZE

        self.canvas = tk.Canvas(
            master, width=width, height=height, bg=COLOR_BG, highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        # status line + New‑Game button ---------------------------------
        self.status = tk.Label(master, text="", font=("Helvetica", 14))
        self.status.pack()

        tk.Button(
            master, text="New Game", command=self.new_game, font=("Helvetica", 12)
        ).pack(pady=6)

        # initial board -------------------------------------------------
        self._draw_board()
        self._update_status()

    # ──────────────────────────────────────────────────────────────────
    #  Event handlers
    # ──────────────────────────────────────────────────────────────────
    def on_click(self, event: tk.Event) -> None:
        """Drop a disc into the clicked column."""
        if self.engine.game_over:
            return

        col = event.x // CELL_SIZE
        try:
            row, col = self.engine.drop_piece(col)
        except ValueError:
            # illegal column or column full – just ignore the click
            return

        self._draw_disc(row, col)
        self._update_status()

    def new_game(self) -> None:
        """Reset the board and start over."""
        self.engine.reset()
        self.canvas.delete("disc")   # remove every previously drawn disc
        self._update_status()

    # ──────────────────────────────────────────────────────────────────
    #  Drawing helpers
    # ──────────────────────────────────────────────────────────────────
    def _draw_board(self) -> None:
        """Blue background + white ‘holes’ once at start‑up."""
        w = ConnectFour.COLS * CELL_SIZE
        h = ConnectFour.ROWS * CELL_SIZE
        self.canvas.create_rectangle(0, 0, w, h, fill=COLOR_BG, width=0)

        for r in range(ConnectFour.ROWS):
            for c in range(ConnectFour.COLS):
                self._draw_hole(r, c)

    def _draw_hole(self, r: int, c: int) -> None:
        x0 = c * CELL_SIZE + DISC_OUTLINE
        y0 = r * CELL_SIZE + DISC_OUTLINE
        x1 = x0 + CELL_SIZE - 2 * DISC_OUTLINE
        y1 = y0 + CELL_SIZE - 2 * DISC_OUTLINE
        self.canvas.create_oval(x0, y0, x1, y1, fill=COLOR_EMPTY, width=0)

    def _draw_disc(self, row: int, col: int) -> None:
        """
        Paint a disc at (row, col).  **Row 0 is the *top* of the numpy board,
        so we draw it the same way here – the engine already gives us the
        bottom‑most free row first, which is exactly what we want.**
        """
        x0 = col * CELL_SIZE + DISC_OUTLINE
        y0 = row * CELL_SIZE + DISC_OUTLINE
        x1 = x0 + CELL_SIZE - 2 * DISC_OUTLINE
        y1 = y0 + CELL_SIZE - 2 * DISC_OUTLINE

        piece = int(self.engine.board[row, col])
        color = COLOR_P1 if piece == ConnectFour.PLAYER1 else COLOR_P2

        self.canvas.create_oval(
            x0, y0, x1, y1, fill=color, width=DISC_OUTLINE, tags="disc"
        )

    # ──────────────────────────────────────────────────────────────────
    #  Status line
    # ──────────────────────────────────────────────────────────────────
    def _update_status(self) -> None:
        if self.engine.game_over:
            if self.engine.winner:
                self.status.config(text=f"Player {self.engine.winner} wins!")
            else:
                self.status.config(text="Draw!")
        else:
            self.status.config(text=f"Player {self.engine.current_player}'s turn")


# ──────────────────────────────────────────────────────────────────────
#  Stand‑alone launch
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    ConnectFourGUI(root)
    root.mainloop()
