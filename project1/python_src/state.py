import numpy as np

WHITE, BLACK, EMPTY = 1, 2, 0

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


if __name__ == "__main__":
    import numpy as np
    WHITE, BLACK, EMPTY = 1, 2, 0
    one_step = 1
    two_steps = 2
    width, height = 10,10
    board = np.zeros((height, width), dtype=np.float64)
    board[:2,:] = WHITE
    board[height-2:,:] = BLACK
    print(board)

    dash_count = width*4 - 3
    line = "\n" + "-"*dash_count + "\n"
    print(line.join([" | ".join(str(cell) for cell in row) for row in board[::-1]]))
    print(type(board))
    t = 100
    indices = np.where(board == WHITE)
    result = list(zip(indices[1], indices[0]))
    print(result)
    def addd(t,x,y):
        return x+y+t
    for i in result:
        print(addd(t,*i))
    print(board[0,:])
    indices = np.where(board == BLACK)
    rows, _ = indices
    min_distance = np.min(rows)
    print(min_distance)
    indices = np.where(board == WHITE)
    rows, _ = indices
    min_distance = np.max(rows)
    print(4-min_distance)
    num_black = np.count_nonzero(board == BLACK)
    board[3,1] = WHITE
    print(board)
    black_rows, _ = np.where(board == BLACK)
    white_rows, _ = np.where(board == WHITE)
    print(height-1-black_rows)
    print(white_rows)

