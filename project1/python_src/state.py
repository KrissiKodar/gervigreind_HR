
WHITE, BLACK, EMPTY = "W", "B", " "

class State:  
	def __init__(self, width, height) -> None:
		self.board = [[WHITE]*width if i < 2 else
					  [BLACK]*width if i > height-3 else
					  [EMPTY]*width for i in range(height)]
		
		self.white_turn = True
		self.width = width
		
	def __str__(self) -> str:
		dash_count = self.width*4 - 3
		line = "\n" + "-"*dash_count + "\n"
		return line.join([" | ".join(cell for cell in row) for row in self.board[::-1]])
	
	