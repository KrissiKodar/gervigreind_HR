
WHITE, BLACK, EMPTY = "W", "B", " "

class State:  
    def __init__(self, width, height) -> None:
        self.board = [[WHITE]*width if i < 2 else
                      [BLACK]*width if i > height-3 else
                      [EMPTY]*width for i in range(height)]
        
        self.white_turn = True
        self.width = width
        self.height = height
        
    def __str__(self) -> str:
        dash_count = self.width*4 - 3
        line = "\n" + "-"*dash_count + "\n"
        return line.join([" | ".join(cell for cell in row) for row in self.board[::-1]])
    
if __name__ == "__main__":
    k = 0
    h = 0
    height = 5
    width = 5
    board = [[WHITE]*width if i < 2 else
                      [BLACK]*width if i > height-3 else
                      [EMPTY]*width for i in range(height)]
    for idx, i in enumerate(reversed(board)):
        if WHITE in i:
            k += 1+height - idx
            break    
    for idx, i in enumerate(board):
        if BLACK in i:
            h += 1+height - idx
            break
    print(k)
    print(h)