import collections
import re
from enum import IntEnum

from state import State

import time

WHITE, BLACK, EMPTY = "W", "B", " "


class Environment:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.current_state = State(width, height)
    
    def can_move_n_steps_forward(self, state, y, max_height_black, max_height_white):
        if state.white_turn:
            return y <= max_height_white
        else:
            return y >= max_height_black
        
    def get_moves(self, state, move, y, x):
        opponent = BLACK if state.white_turn else WHITE
        one_step = 1 if state.white_turn else -1
        two_steps = 2 if state.white_turn else -2
        
        # two steps forward and one step left/right
        if self.can_move_n_steps_forward(state, y, 2, self.height - 3):
            if x > 0 and state.board[y + two_steps][x - 1] == EMPTY:
                move.append((x, y, x - 1, y + two_steps))
            if x < self.width - 1 and state.board[y + two_steps][x + 1] == EMPTY:
                move.append((x, y, x + 1, y + two_steps))
            
        # one step forward and two step left/right
        if self.can_move_n_steps_forward(state, y, 1, self.height - 2):
            if x > 1 and state.board[y + one_step][x - 2] == EMPTY:
                move.append((x, y, x - 2, y + one_step))
            if x < self.width - 2 and state.board[y + one_step][x + 2] == EMPTY:
                move.append((x, y, x + 2, y + one_step))	
            # kill opponent, only one step diagonal forward
            if x > 0 and state.board[y + one_step][x - 1] == opponent:
                move.append((x, y, x - 1, y + one_step))
            if x < self.width - 1 and state.board[y + one_step][x + 1] == opponent:
                move.append((x, y, x + 1, y + one_step))


        
    def get_legal_moves(self, state):
        moves = []
        friendly = WHITE if state.white_turn else BLACK
        #t_start = time.time()
        for y in range(self.height):
            for x in range(self.width):
                if state.board[y][x] == friendly:
                    self.get_moves(state, moves, y, x)

        #friendly_pieces = [(y, x) for y in range(self.height) for x in range(self.width) if state.board[y][x] == friendly]
        #for y, x in friendly_pieces:
        #    self.get_moves(state, moves, y, x)
        #t_end = time.time()
        #print("Time to get legal moves: ", t_end - t_start)
        return moves

    def move(self, state, move):
        x1, y1, x2, y2 = move
        state.board[y2][x2], state.board[y1][x1] = state.board[y1][x1], EMPTY
        state.white_turn = not state.white_turn

    def was_diagonal_move(self, move):
        x1, y1, x2, y2 = move
        if y2 - 1 == y1 and x2 - 1 == x1:
            return True
        if y2 - 1 == y1 and x2 + 1 == x1:
            return True
        if y2 + 1 == y1 and x2 - 1 == x1:
            return True
        if y2 + 1 == y1 and x2 + 1 == x1:
            return True
        return False
        
    def undo_move(self, state, move):
        x1, y1, x2, y2 = move

        if self.was_diagonal_move(move):
            if state.white_turn:
                state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], WHITE
            else:
                state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], BLACK
        else: # not diagonal move
            state.board[y1][x1], state.board[y2][x2] = state.board[y2][x2], state.board[y1][x1]
        
        state.white_turn = not state.white_turn

    def is_terminal(self, state):
        if state.white_turn:
            y = self.height - 1
            for x in range(self.width):
                if state.board[y][x] == WHITE:
                    return True
        elif not state.white_turn:
            y = 0
            for x in range(self.width):
                if state.board[y][x] == BLACK:
                    return True
        elif len(self.get_legal_moves(state)) == 0:
            return True
        return False        


if __name__ == "__main__":
    def foo(hehe):
        return True
    
    def bla(game, state):
        foo(game.move(state, (0, 0, 0, 2)))
        print(state)
        print(game.get_legal_moves(state))
        print("is terminal: ", game.is_terminal(state))
        game.undo_move(state, (0, 0, 0, 2))
        print(state)
        print(game.get_legal_moves(state))
        print("is terminal: ", game.is_terminal(state))
        print()
    env = Environment(3, 5)
    print(env.get_legal_moves(env.current_state))
    bla(env, env.current_state)

