import collections
import re
from enum import IntEnum

from state import State

import time
from numpy import where

WHITE, BLACK, EMPTY = 1, 2, 0


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
        
    def get_moves(self, state, y, x):
        # get opponent
        opponent = BLACK if state.white_turn else WHITE
        
        # get one step and two steps
        one_step = 1 if state.white_turn else -1
        two_steps = 2 if state.white_turn else -2
        
        # two steps forward and one step left/right
        if (state.white_turn and y <= self.height - 3) or (not state.white_turn and y >= 2):
            if x > 0 and state.board[y + two_steps, x - 1] == EMPTY:
                yield (x, y, x - 1, y + two_steps)
            if x < self.width - 1 and state.board[y + two_steps, x + 1] == EMPTY:
                yield (x, y, x + 1, y + two_steps)
            
        # one step forward and two step left/right
        if (state.white_turn and y <= self.height - 2) or (not state.white_turn and y >= 1):
            if x > 1 and state.board[y + one_step, x - 2] == EMPTY:
                yield (x, y, x - 2, y + one_step)
            if x < self.width - 2 and state.board[y + one_step, x + 2] == EMPTY:
                yield (x, y, x + 2, y + one_step)	
            # kill opponent, only one step diagonal forward
            if x > 0 and state.board[y + one_step, x - 1] == opponent:
                yield (x, y, x - 1, y + one_step)
            if x < self.width - 1 and state.board[y + one_step, x + 1] == opponent:
                yield (x, y, x + 1, y + one_step)

############################
    def get_legal_moves(self, state):
        friendly = WHITE if state.white_turn else BLACK
        friendly_indices = where(state.board == friendly)
        for i in list(zip(friendly_indices[0], friendly_indices[1]))[::-1 if state.white_turn else 1]:
            yield from self.get_moves(state, *i)


    def move(self, state, move):
        x1, y1, x2, y2 = move
        state.board[y2,x2], state.board[y1,x1] = state.board[y1,x1], EMPTY
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
                state.board[y1,x1], state.board[y2,x2] = BLACK, WHITE
            else:
                state.board[y1,x1], state.board[y2,x2] = WHITE, BLACK
        else: # not diagonal move
            state.board[y1,x1], state.board[y2,x2] = state.board[y2,x2], state.board[y1,x1] 
        state.white_turn = not state.white_turn

    def is_terminal(self, state):
        if any(state.board[-1,:] == WHITE):
            return True, WHITE
        if any(state.board[0,:] == BLACK):
            return True, BLACK
        #return False, None
        try:
            # check if there are any legal moves
            next(self.get_legal_moves(state))
            return False, None
        except StopIteration:
            # no legal moves, draw
            return True, 0
    
    
    def count_attacks(self, state, opponent, one_step, y, x):
        n = 0
        if (state.white_turn and y <= self.height - 2) or (not state.white_turn and y >= 1):
            if x > 0 and state.board[y + one_step, x - 1] == opponent:
                n += 1
            if x < self.width - 1 and state.board[y + one_step, x + 1] == opponent:
                n += 1
        return n

    def get_n_attacking_moves(self, state):
        friendly = WHITE if state.white_turn else BLACK
        opponent = BLACK if state.white_turn else WHITE
        one_step = 1 if state.white_turn else -1
        n_friendly_attacks = 0
        friendly_indices = where(state.board == friendly)
        for i in list(zip(friendly_indices[0], friendly_indices[1])):
            n_friendly_attacks += self.count_attacks(state, opponent, one_step, *i)	
        return n_friendly_attacks
        

    


if __name__ == "__main__":
    
    env = Environment(5, 5)
    env.move(env.current_state, (0, 0, 1, 2))
    env.move(env.current_state, (4, 4, 3, 2))
    #print(env.current_state.board)
    #for i in env.get_legal_moves(env.current_state):
    #    print(i)
    
    #print(env.get_n_attacking_moves(env.current_state))
    
    import timeit
    
    def my_function():
        for i in env.get_legal_moves(env.current_state):
            pass
        
    n = 1
    total_time = timeit.timeit(my_function, number=n)
    average_time = total_time / n
    print("Average time: ", average_time)
    


