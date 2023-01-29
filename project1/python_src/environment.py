import collections
import re
from enum import IntEnum

from state import State

WHITE, BLACK, EMPTY = "W", "B", " "


class Environment:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.current_state = State(width, height)

    def get_legal_moves(self, state):
        pass

    def move(self, state, move):
        x1, x2, y1, y2 = move
        state.board[y2][x2], state.board[y1][x1] = state.board[y1][x1], state.board[y2][x2]
        state.white_turn = not state.white_turn

    def undo_move(self, state, move):
        x1, x2, y1, y2 = move

        if self.was_diagonal_move(move):
            state.board[y1][x1] = state.board[y2][x2]
            state.board[y2][x2] = EMPTY
        import numpy as np
        a = np.random.rand(3,3)
        print(a.flatten())
        