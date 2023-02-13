import numpy as np

WHITE, BLACK, EMPTY = 1, 2, 0


# changed the state to a numpy array
# seemed to make the code run faster
# according to my tests.
class State:  
    def __init__(self, width, height) -> None:
        self.board = np.zeros((height, width), dtype=int)
        self.board[:2,:] = WHITE
        self.board[height-2:,:] = BLACK
        
        self.white_turn = True
        self.width = width
        self.height = height
        
    def __str__(self) -> str:
        dash_count = self.width*4 - 3
        line = "\n" + "-"*dash_count + "\n"
        return line.join([" | ".join(str(cell) for cell in row) for row in self.board[::-1]])
    
    def __hash__(self):
        """to add position to visited set"""
        return hash(str(self))

    