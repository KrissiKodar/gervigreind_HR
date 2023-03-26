import numpy as np
import itertools
import time

# utility functions for various solvers
class nonogram_solver:
	def __init__(self, row_constraints, col_constraints):
		self.row_constraints = row_constraints
		self.col_constraints = col_constraints
  
	# check if solution
	def is_valid(self, puzzle):
		for r, row in enumerate(puzzle):
			row_groups = [len(list(group)) for key, group in itertools.groupby(row) if key == 1]
			if row_groups != self.row_constraints[r] and self.row_constraints[r] != [0]:
				return False

		for c, col in enumerate(zip(*puzzle)):
			col_groups = [len(list(group)) for key, group in itertools.groupby(col) if key == 1]
			if col_groups != self.col_constraints[c] and self.col_constraints[c] != [0]:
				return False
		return True

	def max_n_groups(self, x):
		return np.ceil(x / 2)
	
	def count_groups(self, row_or_col):
		return len([group for key, group in itertools.groupby(row_or_col) if key == 1])

# start at top left and work down, rows first
# checks if the row or column sums are larger than the sum of the constraints
# checks if the number of row or column groups is larger than the number of groups in the constraints
#
# when every variable has been assigned it checks if the solution is a valid solution
# (backtracks if it is not)
# backtracks at when every variable has been assigned and the solution is not valid
class BF(nonogram_solver):
	def __init__(self, puzzle, row_constraints, col_constraints):
		super().__init__(row_constraints, col_constraints)
		self.n_rows = puzzle.shape[0]
		self.n_cols = puzzle.shape[1]
		self.n_cells = self.n_rows * self.n_cols
     
		self.row_constraints = row_constraints
		self.row_sums = [np.sum(row) for row in self.row_constraints]
		self.row_groups = [len(row) for row in self.row_constraints]
  
		self.col_constraints = col_constraints
		self.col_sums = [np.sum(col) for col in self.col_constraints]
		self.col_groups = [len(col) for col in self.col_constraints]
  
		self.assignment = {}
		self.states_visited = 0

	def is_consistent(self, puzzle):
		#row sums and groups
		for i, row in enumerate(puzzle):
			sum_row = np.sum(row)
			row_groups = super().count_groups(row)
			if sum_row > self.row_sums[i]:
				return False
			if row_groups > self.row_groups[i]:
				return False
			if sum_row == self.row_sums[i] and row_groups < self.row_groups[i]:
				return False

		#column sums and groups
		for i, col in enumerate(puzzle.T):
			sum_col = np.sum(col)
			col_groups = super().count_groups(col)
			if sum_col > self.col_sums[i]:
				return False
			if col_groups > self.col_groups[i]:
				return False
			if sum_col == self.col_sums[i] and col_groups < self.col_groups[i]:
				return False
			
		return True

	def start_search(self, puzzle):
		return self.backtracking_search(puzzle)

	def backtracking_search(self, puzzle, position = (0,0)):
		# if assignment is complete then return assignment
		if len(self.assignment) == self.n_cells:
			if super().is_valid(puzzle):
				return self.assignment
			return False

		# select unassigned variable
		current_cell = position
		self.states_visited += 1
  
		for i in [1, 0]:
			puzzle[current_cell] = i
			if self.is_consistent(puzzle, current_cell):
				self.assignment[current_cell] = i
				next_col = (current_cell[1] + 1) % self.n_cols
				next_row = current_cell[0]+ (current_cell[1] + 1) // self.n_cols
				next_pos = (next_row, next_col)
				result = self.backtracking_search(puzzle, next_pos)
				if result != False:
					return result
				del self.assignment[current_cell]
		return False


class pre_constrain_check(nonogram_solver):
	def __init__(self, puzzle, row_constraints, col_constraints):
		super().__init__(row_constraints, col_constraints)
		self.n_rows = puzzle.shape[0]
		self.n_cols = puzzle.shape[1]
		self.n_cells = self.n_rows * self.n_cols
     
		self.row_constraints = row_constraints
		self.row_sums = [np.sum(row) for row in self.row_constraints]
		self.row_groups = [len(row) for row in self.row_constraints]
  
		self.col_constraints = col_constraints
		self.col_sums = [np.sum(col) for col in self.col_constraints]
		self.col_groups = [len(col) for col in self.col_constraints]
  
		self.assignment = {}
		self.states_visited = 0

		# pre-constrain check
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				self.assignment[(i, j)] = None

		# check how many groups of filled in cells can fit in the row or column
		# if the number of groups in the constraint is equal to the number of groups that can fit in the row or column
		# then fill the row or column accordingly
		max_n_row_groups = super().max_n_groups(self.n_rows)
		max_n_colgroups = super().max_n_groups(self.n_rows)
		for i, row_group_size in enumerate(self.row_groups):
			if row_group_size == max_n_row_groups:
				if self.n_cols % 2 == 1:
					for j in range(self.n_cols):
						if j % 2 == 0:
							self.assignment[(i, j)] = 1
						else:
							self.assignment[(i, j)] = 0
				else:
					for j in range(self.n_cols):
						if j % 2 == 0:
							self.assignment[(i, j)] = 0
						else:
							self.assignment[(i, j)] = 1
		for i, col_group_size in enumerate(self.col_groups):
			if col_group_size == max_n_colgroups:
				if self.n_rows % 2 == 1:
					for j in range(self.n_rows):
						if j % 2 == 0:
							self.assignment[(j, i)] = 1
						else:
							self.assignment[(j, i)] = 0
				else:
					for j in range(self.n_rows):
						if j % 2 == 0:
							self.assignment[(j, i)] = 0
						else:
							self.assignment[(j, i)] = 1
       
		# if there is only one group in the constraint and the sum of the constraint is equal to the number of cells in the row or column
		# then fill the row or column accordingly
		for i in range(self.n_rows):
			if self.row_sums[i] == self.n_cols:
				for j in range(self.n_cols):
					self.assignment[(i, j)] = 1
		for i in range(self.n_cols):
			if self.col_sums[i] == self.n_rows:
				for j in range(self.n_rows):
					self.assignment[(j, i)] = 1
     
		temp_puzzle = np.zeros((self.n_rows, self.n_cols))
		for key, value in self.assignment.items():
			if value != None:
				temp_puzzle[key] = value
		#print(temp_puzzle)
		# forwards checking
		for i, row in enumerate(temp_puzzle):
			if np.sum(row) == self.row_sums[i] and super().count_groups(row) == self.row_groups[i]:
				# assign values from temp_puzzle row to self.assignment
				for j, value in enumerate(row):
					self.assignment[(i, j)] = value
		for i, col in enumerate(temp_puzzle.T):
			if np.sum(col) == self.col_sums[i] and super().count_groups(col) == self.col_groups[i]:
				# assign values from temp_puzzle col to self.assignment
				for j, value in enumerate(col):
					self.assignment[(j, i)] = value
		#print(self.assignment) 

	def is_consistent(self, puzzle):
		#row sums and groups
		for i, row in enumerate(puzzle):
			sum_row = np.sum(row)
			row_groups = super().count_groups(row)
			if sum_row > self.row_sums[i]:
				return False
			if row_groups > self.row_groups[i]:
				return False
			if sum_row == self.row_sums[i] and row_groups < self.row_groups[i]:
				return False

		#column sums and groups
		for i, col in enumerate(puzzle.T):
			sum_col = np.sum(col)
			col_groups = super().count_groups(col)
			if sum_col > self.col_sums[i]:
				return False
			if col_groups > self.col_groups[i]:
				return False
			if sum_col == self.col_sums[i] and col_groups < self.col_groups[i]:
				return False
			
		return True

	def start_search(self, puzzle):
		# where dictionary is not None assign values to puzzle
		for key, value in self.assignment.items():
			if value != None:
				puzzle[key] = value
		print("before starting search:")
		print(puzzle)
		print("\n\n\n")
		return self.backtracking_search(puzzle)

	def backtracking_search(self, puzzle):
		# if assignment is complete then return assignment
		if None not in self.assignment.values():
			if super().is_valid(puzzle):
				return self.assignment
			print("invalid solution, backtracking...")
			return False

  		# select unassigned variable
		#current_cell = position
		# select next key in dictionary which has a value of None
		for key, value in self.assignment.items():
			if value == None:
				current_cell = key
				break
		self.states_visited += 1

		# if variable has a value in the assignment then skip (it has already been assigned in the pre-solver)
		# if self.assignment[current_cell] != None:
		#	return self.backtracking_search(puzzle)
		for i in [1, 0]:
			puzzle[current_cell] = i
			print("\n\n")
			print(puzzle)
			print("current cell = ", current_cell)
			# print unassigned variables
			print("unassigned variables:")
			for key, value in self.assignment.items():
				if value == None:
					print(key)
			print("\n\n")
			if self.is_consistent(puzzle):
				self.assignment[current_cell] = i
				result = self.backtracking_search(puzzle)
				if result != False:
					return result
				self.assignment[current_cell] = None
		print("backtracking...")
		return False

class pre_constrain_check_forward_check(nonogram_solver):
	def __init__(self, puzzle, row_constraints, col_constraints):
		super().__init__(row_constraints, col_constraints)
		self.n_rows = puzzle.shape[0]
		self.n_cols = puzzle.shape[1]
		self.n_cells = self.n_rows * self.n_cols
     
		self.row_constraints = row_constraints
		self.row_sums = [np.sum(row) for row in self.row_constraints]
		self.row_groups = [len(row) for row in self.row_constraints]
  
		self.col_constraints = col_constraints
		self.col_sums = [np.sum(col) for col in self.col_constraints]
		self.col_groups = [len(col) for col in self.col_constraints]
  
		self.assignment = {}
		self.states_visited = 0

		# pre-constrain check
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				self.assignment[(i, j)] = None

		# check how many groups of filled in cells can fit in the row or column
		# if the number of groups in the constraint is equal to the number of groups that can fit in the row or column
		# then fill the row or column accordingly
		max_n_row_groups = super().max_n_groups(self.n_rows)
		max_n_colgroups = super().max_n_groups(self.n_rows)
		for i, row_group_size in enumerate(self.row_groups):
			if row_group_size == max_n_row_groups:
				if self.n_cols % 2 == 1:
					for j in range(self.n_cols):
						if j % 2 == 0:
							self.assignment[(i, j)] = 1
						else:
							self.assignment[(i, j)] = 0
				else:
					for j in range(self.n_cols):
						if j % 2 == 0:
							self.assignment[(i, j)] = 0
						else:
							self.assignment[(i, j)] = 1
		for i, col_group_size in enumerate(self.col_groups):
			if col_group_size == max_n_colgroups:
				if self.n_rows % 2 == 1:
					for j in range(self.n_rows):
						if j % 2 == 0:
							self.assignment[(j, i)] = 1
						else:
							self.assignment[(j, i)] = 0
				else:
					for j in range(self.n_rows):
						if j % 2 == 0:
							self.assignment[(j, i)] = 0
						else:
							self.assignment[(j, i)] = 1
       
		# if there is only one group in the constraint and the sum of the constraint is equal to the number of cells in the row or column
		# then fill the row or column accordingly
		for i in range(self.n_rows):
			if self.row_sums[i] == self.n_cols:
				for j in range(self.n_cols):
					self.assignment[(i, j)] = 1
		for i in range(self.n_cols):
			if self.col_sums[i] == self.n_rows:
				for j in range(self.n_rows):
					self.assignment[(j, i)] = 1
     
		temp_puzzle = np.zeros((self.n_rows, self.n_cols))
		for key, value in self.assignment.items():
			if value != None:
				temp_puzzle[key] = value
		#print(temp_puzzle)
		# forwards checking
		for i, row in enumerate(temp_puzzle):
			if np.sum(row) == self.row_sums[i] and super().count_groups(row) == self.row_groups[i]:
				# assign values from temp_puzzle row to self.assignment
				for j, value in enumerate(row):
					self.assignment[(i, j)] = value
		for i, col in enumerate(temp_puzzle.T):
			if np.sum(col) == self.col_sums[i] and super().count_groups(col) == self.col_groups[i]:
				# assign values from temp_puzzle col to self.assignment
				for j, value in enumerate(col):
					self.assignment[(j, i)] = value
		#print(self.assignment) 

	def is_consistent(self, puzzle):
		#row sums and groups
		for i, row in enumerate(puzzle):
			sum_row = np.sum(row)
			row_groups = super().count_groups(row)
			if sum_row > self.row_sums[i]:
				return False
			if row_groups > self.row_groups[i]:
				return False
			if sum_row == self.row_sums[i] and row_groups < self.row_groups[i]:
				return False

		#column sums and groups
		for i, col in enumerate(puzzle.T):
			sum_col = np.sum(col)
			col_groups = super().count_groups(col)
			if sum_col > self.col_sums[i]:
				return False
			if col_groups > self.col_groups[i]:
				return False
			if sum_col == self.col_sums[i] and col_groups < self.col_groups[i]:
				return False
			
		return True

	def start_search(self, puzzle):
		# where dictionary is not None assign values to puzzle
		for key, value in self.assignment.items():
			if value != None:
				puzzle[key] = value
		print("before starting search:")
		print(puzzle)
		print("\n\n\n")
		return self.backtracking_search(puzzle)

	def forward_checking(self, puzzle):
		# forwards checking
		for i, row in enumerate(puzzle):
			if np.sum(row) == self.row_sums[i] and super().count_groups(row) == self.row_groups[i]:
				# assign values from puzzle row to self.assignment
				for j, value in enumerate(row):
					self.assignment[(i, j)] = value
		for i, col in enumerate(puzzle.T):
			if np.sum(col) == self.col_sums[i] and super().count_groups(col) == self.col_groups[i]:
				# assign values from puzzle col to self.assignment
				for j, value in enumerate(col):
					self.assignment[(j, i)] = value


	def backtracking_search(self, puzzle):
		# if assignment is complete then return assignment
		if None not in self.assignment.values():
			if super().is_valid(puzzle):
				return self.assignment
			return False

  		# select unassigned variable
		#current_cell = position
		# select next key in dictionary which has a value of None
		for key, value in self.assignment.items():
			if value == None:
				current_cell = key
				break
		self.states_visited += 1

		# if variable has a value in the assignment then skip (it has already been assigned in the pre-solver)
		# if self.assignment[current_cell] != None:
		#	return self.backtracking_search(puzzle)
		for i in [1, 0]:
			puzzle[current_cell] = i
			print("\n\n")
			print(puzzle)
			print("current cell = ", current_cell)
			# print unassigned variables
			print("unassigned variables:")
			for key, value in self.assignment.items():
				if value == None:
					print(key)
			print("\n\n")
			if self.is_consistent(puzzle):
				self.assignment[current_cell] = i
				result = self.backtracking_search(puzzle)
				if result != False:
					return result
				self.assignment[current_cell] = None
		print("backtracking")
		return False

def test_solver(solver, row_constraints, col_constraints):
	puzzle = np.zeros((len(row_constraints), len(col_constraints)))
	start_time = time.time()	
	current_solver = solver(puzzle, row_constraints, col_constraints)
	assignments = current_solver.start_search(puzzle)
	end = time.time()
	print(f"Time taken = {end - start_time} s")
	print(assignments)
	print(f"States visited = {current_solver.states_visited}")
	for row in range(puzzle.shape[0]):
		for col in range(puzzle.shape[1]):
			if assignments[(row, col)] == 1:
				print(" #", end="")
			else:
				print(" .", end="")
		print()
	print("Solver finished\n\n")
 
if __name__ == '__main__':
	print("################ PROGRAM START #################\n\n")
	row_constraints = [[1], [1],   [2],   [1,1,1], [1,2]]
	col_constraints = [[2], [1,1], [3],   [1,1],   [1]]
 
	#row_constraints = [[1], [1,1],   [1],   [1], [5]]
	#col_constraints = [[2], [2,1], [1],   [1,1],   [1,1]]
 
	#row_constraints = [[7], [1,1,2], [1,1,1,1], [1,2,1], [1,1,1,1], [1,1,2], [7]]
	#col_constraints = [[7], [1,1], [7], [1,1,1], [1,1,1,1], [2,2], [7]]	
	
	#row_constraints = [[4,2], [2], [2,4], [1,2], [7], [3,2], [1,3,2], [2,3], [3,2], [3,2]]
	#col_constraints = [[2], [1,1], [3], [3,1], [1,6], [6], [1,8], [1,1,1], [5,2], [5,2]]
	
	

	#test_solver(BF, row_constraints, col_constraints)
	#test_solver(pre_constrain_check, row_constraints, col_constraints)
	test_solver(pre_constrain_check_forward_check, row_constraints, col_constraints)
	
	#puzzle = np.zeros((len(row_constraints), len(col_constraints)))
	#ttt = pre_constrain_check(puzzle, row_constraints, col_constraints)
	#print(ttt.assignment)
	

	

	
	

