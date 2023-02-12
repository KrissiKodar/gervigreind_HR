import collections
import re
from enum import IntEnum

from state import State

import time
import numpy as np
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
        
    def get_moves(self, board, whites_turn, y, x):
        
        # I removed can_move_n_steps_forward calls to reduce the number of function calls
        
        # get opponent
        opponent = BLACK if whites_turn else WHITE
        
        # get one step and two steps
        one_step = 1 if whites_turn else -1
        two_steps = 2 if whites_turn else -2
        
        # trying to speed up the code, avoiding duplicate calculations
        x_bigger_than_0 = x > 0
        x_less_than_width_minus_1 = x < self.width - 1
        
        x_minus_1 = x - 1
        x_plus_1 = x + 1
        x_plus_2 = x + 2
        x_minus_2 = x - 2
        y_plus_one_step = y + one_step
        y_plus_two_steps = y + two_steps
        
        # two steps forward and one step left/right
        if (whites_turn and y <= self.height - 3) or (not whites_turn and y >= 2):
            if x_bigger_than_0 and board[y_plus_two_steps, x_minus_1] == EMPTY:
                yield (x, y, x_minus_1, y_plus_two_steps)
            if x_less_than_width_minus_1 and board[y_plus_two_steps, x_plus_1] == EMPTY:
                yield (x, y, x_plus_1, y_plus_two_steps)
            
        # one step forward and two step left/right
        if (whites_turn and y <= self.height - 2) or (not whites_turn and y >= 1):
            if x > 1 and board[y_plus_one_step, x_minus_2] == EMPTY:
                yield (x, y, x_minus_2, y_plus_one_step)
            if x < self.width - 2 and board[y_plus_one_step, x_plus_2] == EMPTY:
                yield (x, y, x_plus_2, y_plus_one_step)	
            # kill opponent, only one step diagonal forward
            if x_bigger_than_0 and board[y_plus_one_step, x_minus_1] == opponent:
                yield (x, y, x_minus_1, y_plus_one_step)
            if x_less_than_width_minus_1 and board[y_plus_one_step, x_plus_1] == opponent:
                yield (x, y, x_plus_1, y_plus_one_step)
        
        

############################
    def get_legal_moves(self, state):
        whites_turn = state.white_turn
        the_board = state.board
        friendly = WHITE if whites_turn else BLACK
        friendly_indices = where(the_board  == friendly)
        for i in list(zip(friendly_indices[0], friendly_indices[1]))[::-1 if whites_turn else 1]:
            yield from self.get_moves(the_board, whites_turn, *i)


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
    import numpy as np
    g = np.array([0, 0, 0, 0, 0])
    #print(env.get_n_attacking_moves(env.current_state))
    print(type(g))
    print(type(env.current_state.board))
    import timeit
    
    def my_function():
        for i in env.get_legal_moves(env.current_state):
            pass
        
    n = 100000
    total_time = timeit.timeit(my_function, number=n)
    average_time = total_time / n
    print("Average time: ", average_time)
    print("Total time: ", total_time)
    
    #import cProfile
    
    #cProfile.run('my_function()')


