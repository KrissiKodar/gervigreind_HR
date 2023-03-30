import numpy as np
import itertools
import time
import random

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

	# check if row is valid
	def is_valid_row(self, row, row_index):
		row_groups = [len(list(group)) for key, group in itertools.groupby(row) if key == 1]
		if row_groups != self.row_constraints[row_index] and self.row_constraints[row_index] != [0]:
			return False
		return True

	# check if column is valid
	def is_valid_col(self, col, col_index):
		col_groups = [len(list(group)) for key, group in itertools.groupby(col) if key == 1]
		if col_groups != self.col_constraints[col_index] and self.col_constraints[col_index] != [0]:
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

		# fill in self.assignment with all possible assignments
		for i in range(self.n_rows):
			for j in range(self.n_cols):
				self.assignment[(i, j)] = None
     

	def print_assignment(self, assignment):
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				if assignment[(row, col)] == 1:
					print(" #", end="")
				if assignment[(row, col)] == 0:
					print(" .", end="")
				elif assignment[(row, col)] == None:
					print(" x", end="")
			print()
		print()
  
	def is_consistent(self, puzzle, assignment_temp):
		#row sums and groups
		for i, row in enumerate(puzzle):
			sum_row = np.sum(row)
			row_groups = super().count_groups(row)
			if sum_row > self.row_sums[i]:
				return False
			if row_groups > self.row_groups[i]:
				return False
				 

		#column sums and groups
		for i, col in enumerate(puzzle.T):
			sum_col = np.sum(col)
			col_groups = super().count_groups(col)
			if sum_col > self.col_sums[i]:
				return False
			if col_groups > self.col_groups[i]:
				return False
		return True

	def start_search(self, puzzle):
		# where dictionary is not None assign values to puzzle
		for key, value in self.assignment.items():
			if value != None:
				puzzle[key] = value
		print("before starting search:")
		self.print_assignment(self.assignment)
		print("------------------------")
		return self.backtracking_search(puzzle)

	def backtracking_search(self, puzzle):
		# if assignment is complete then return assignment
		if None not in self.assignment.values():
			if super().is_valid(puzzle):
				return self.assignment
			#print("invalid solution, backtracking...")
			return False

  		# select unassigned variable
		# current_cell = position
		# select next key in dictionary which has a value of None
		for key, value in self.assignment.items():
			if value == None:
				current_cell = key
				#print("current cell = ", current_cell)
				break

		self.states_visited += 1
		if self.states_visited % 10000 == 0:
			self.print_assignment(self.assignment)
			print("states visited: ", self.states_visited)
			print("current cell = ", current_cell)
			print("\n\n")

		assignment_temp = self.assignment.copy()
  

		# Order domain values
		values_list = [1, 0]
		#random.shuffle(values_list)
		#alues_list = random.choices([[1, 0], [0, 1]], weights=[0.85, 0.15])[0]
		for i in values_list:
			temp_puzzle = puzzle.copy()
			temp_puzzle[current_cell] = i
			assignment_temp[current_cell] = i
			if self.is_consistent(temp_puzzle, assignment_temp):
				self.assignment[current_cell] = i
				#self.forward_checking(puzzle)
				result = self.backtracking_search(temp_puzzle)
				if result != False:
					return result
				self.assignment[current_cell] = None
		#print("backtracking...")
		return False



# backtracking with prechecking
class backtracking_with_prechecking(nonogram_solver):
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
     
		#simple boxes
		for i, row in enumerate(puzzle):
			index = 0
			block = 1
			row_copy = row.copy()
			for j in row_constraints[i]:
				for k in range(j):
					row_copy[index] = block
					index += 1
				index += 1
				block += 1
			for k in range(len(row_copy)-1, -1, -1):
				if row_copy[k] != 0:
					shift_by = len(row_copy) - k - 1
					break
			# shift list row by shift_by to the right
			row_copy = list(row_copy)
			row_shifted = row_copy[-shift_by:] + row_copy[:-shift_by]
			result = [1 if ((row_copy[i] != 0 and row_shifted[i] != 0) and (row_copy[i] == row_shifted[i])) else 0 for i in range(min(len(row_copy), len(row_shifted)))]
			# where result is 1 make self.assignment[(i, m)] = 1
			for m, value in enumerate(result):
				if value == 1:
					self.assignment[(i, m)] = 1
     
			# simple spaces			
			row_groups = [len(list(group)) for key, group in itertools.groupby(result) if key == 1]
			if len(row_groups) == len(self.row_constraints[i]):
				test = [0]*len(result)
				group_fill = 1
				padding_list = []
				for j in range(len(row_groups)):
					padding_list.append(self.row_constraints[i][j] - row_groups[j])
				for k in range(len(row)):
					# row = [0,1,1,0,0,0,1,1,1,0,0,0,1,0,0] becomes [0,1,1,0,0,0,2,2,2,0,0,0,3,0,0]
					if result[k] == 1:	
						test[k] = group_fill	
						if k+1 < len(result) and result[k+1] == 0:
							group_fill += 1	
				padded_cells = self.pad_list(test, padding_list)
				# where padded cells are 0 make self.assignment[(i, m)] = 0
				for m, value in enumerate(padded_cells):
					if value == 0:
						self.assignment[(i, m)] = 0
    
		for i, col in enumerate(puzzle.T):
			index = 0
			block = 1
			col_copy = col.copy()
			for j in col_constraints[i]:
				for k in range(j):
					col_copy[index] = block
					index += 1
				index += 1
				block += 1
			for k in range(len(col_copy)-1, -1, -1):
				if col_copy[k] != 0:
					shift_by = len(col_copy) - k - 1
					break
			# shift list row by shift_by to the right
			col_copy = list(col_copy)
			col_shifted = col_copy[-shift_by:] + col_copy[:-shift_by]

			result = [1 if ((col_copy[i] != 0 and col_shifted[i] != 0) and (col_copy[i] == col_shifted[i])) else 0 for i in range(min(len(col_copy), len(col_shifted)))]
			# where result is 1 make self.assignment[(m, i)] = 1
			for m, value in enumerate(result):
				if value == 1:
					self.assignment[(m, i)] = 1
     
			# simple spaces
			col_groups = [len(list(group)) for key, group in itertools.groupby(result) if key == 1]
			if len(col_groups) == len(self.col_constraints[i]):
				test = [0]*len(result)
				group_fill = 1
				padding_list = []
				for j in range(len(col_groups)):
					padding_list.append(self.col_constraints[i][j] - col_groups[j])
				for k in range(len(col)):
					if result[k] == 1:	
						test[k] = group_fill	
						if k+1 < len(result) and result[k+1] == 0:
							group_fill += 1	
				padded_cells = self.pad_list(test, padding_list)
				print("col", i)
				print("padded_cells", padded_cells)
				# where padded cells are 0 make self.assignment[(m, i)] = 0
				for m, value in enumerate(padded_cells):
					if value == 0:
						self.assignment[(m, i)] = 0


		temp_puzzle = np.zeros((self.n_rows, self.n_cols))
		for key, value in self.assignment.items():
			if value != None:
				temp_puzzle[key] = value
    
		#print(temp_puzzle)
		# forward checking
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
	
 
 
	def print_assignment(self, assignment):
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				if assignment[(row, col)] == 1:
					print(" #", end="")
				if assignment[(row, col)] == 0:
					print(" .", end="")
				elif assignment[(row, col)] == None:
					print(" x", end="")
			print()
		print()
  
	def pad_list(self, test, padding_list):
		result = [0] * len(test)
		for i, num in enumerate(test):
			if num != 0:
				padding = padding_list[num - 1]
				for j in range(-padding, padding + 1):
					pos = i + j
					if 0 <= pos < len(test):
						result[pos] = num
		return result
 
	def is_consistent(self, puzzle, assignment_temp):
		#row sums and groups
		for i, row in enumerate(puzzle):
			sum_row = np.sum(row)
			row_groups = super().count_groups(row)
				
			if sum_row > self.row_sums[i]:
				return False
			if sum_row == self.row_sums[i] and row_groups != self.row_groups[i]:
				return False
			# count number of None in assignment_temp for this row
			none_count = 0
			for j in range(self.n_cols):
				if assignment_temp[(i, j)] == None:
					none_count += 1
			if sum_row + none_count < self.row_sums[i]:
				return False
			if none_count == 0:
				if not super().is_valid_row(row, i):
					return False
			#if row_groups > self.row_groups[i]:
			#	return False
				 

		#column sums and groups
		for i, col in enumerate(puzzle.T):
			sum_col = np.sum(col)
			col_groups = super().count_groups(col)
			if sum_col > self.col_sums[i]:
				return False
			if sum_col == self.col_sums[i] and col_groups != self.col_groups[i]:
				return False
			none_count = 0
			for j in range(self.n_rows):
				if assignment_temp[(j, i)] == None:
					none_count += 1
			if sum_col + none_count < self.col_sums[i]:
				return False
			if none_count == 0:
				if not super().is_valid_col(col, i):
					return False
			#if col_groups > self.col_groups[i]:
			#	return False
		return True

	def start_search(self, puzzle):
		# where dictionary is not None assign values to puzzle
		for key, value in self.assignment.items():
			if value != None:
				puzzle[key] = value
		print("before starting search:")
		self.print_assignment(self.assignment)
		print("------------------------")
		return self.backtracking_search(puzzle)

	def backtracking_search(self, puzzle):
		# if assignment is complete then return assignment
		if None not in self.assignment.values():
			if super().is_valid(puzzle):
				return self.assignment
			#print("invalid solution, backtracking...")
			return False

  		# select unassigned variable
		# current_cell = position
		# select next key in dictionary which has a value of None
		for key, value in self.assignment.items():
			if value == None:
				current_cell = key
				#print("current cell = ", current_cell)
				break
		# pick a random cell in self.assignment which has a value of None
		#current_cell = random.choice([key for key, value in self.assignment.items() if value == None])

		self.states_visited += 1

		if self.states_visited % 1 == 0:
			self.print_assignment(self.assignment)
			print("states visited: ", self.states_visited)
			print("current cell = ", current_cell)
			print("\n\n")

		assignment_temp = self.assignment.copy()
  

		# Order domain values
		values_list = [1, 0]
		#random.shuffle(values_list)
		#alues_list = random.choices([[1, 0], [0, 1]], weights=[0.85, 0.15])[0]
		for i in values_list:
			temp_puzzle = puzzle.copy()
			temp_puzzle[current_cell] = i
			assignment_temp[current_cell] = i
			if self.is_consistent(temp_puzzle, assignment_temp):
				self.assignment[current_cell] = i
				result = self.backtracking_search(temp_puzzle)
				if result != False:
					return result
				self.assignment[current_cell] = None
		#print("backtracking...")
		return False

# backtracking with prechecking with added forward checking
class forward_checking(nonogram_solver):
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
     
		#simple boxes
		for i, row in enumerate(puzzle):
			index = 0
			block = 1
			row_copy = row.copy()
			for j in row_constraints[i]:
				for k in range(j):
					row_copy[index] = block
					index += 1
				index += 1
				block += 1
			for k in range(len(row_copy)-1, -1, -1):
				if row_copy[k] != 0:
					shift_by = len(row_copy) - k - 1
					break
			# shift list row by shift_by to the right
			row_copy = list(row_copy)
			row_shifted = row_copy[-shift_by:] + row_copy[:-shift_by]
			result = [1 if ((row_copy[i] != 0 and row_shifted[i] != 0) and (row_copy[i] == row_shifted[i])) else 0 for i in range(min(len(row_copy), len(row_shifted)))]
			# where result is 1 make self.assignment[(i, m)] = 1
			for m, value in enumerate(result):
				if value == 1:
					self.assignment[(i, m)] = 1
     
			# simple spaces			
			row_groups = [len(list(group)) for key, group in itertools.groupby(result) if key == 1]
			if len(row_groups) == len(self.row_constraints[i]):
				test = [0]*len(result)
				group_fill = 1
				padding_list = []
				for j in range(len(row_groups)):
					padding_list.append(self.row_constraints[i][j] - row_groups[j])
				for k in range(len(row)):
					# row = [0,1,1,0,0,0,1,1,1,0,0,0,1,0,0] becomes [0,1,1,0,0,0,2,2,2,0,0,0,3,0,0]
					if result[k] == 1:	
						test[k] = group_fill	
						if k+1 < len(result) and result[k+1] == 0:
							group_fill += 1	
				padded_cells = self.pad_list(test, padding_list)
				# where padded cells are 0 make self.assignment[(i, m)] = 0
				for m, value in enumerate(padded_cells):
					if value == 0:
						self.assignment[(i, m)] = 0
    
		for i, col in enumerate(puzzle.T):
			index = 0
			block = 1
			col_copy = col.copy()
			for j in col_constraints[i]:
				for k in range(j):
					col_copy[index] = block
					index += 1
				index += 1
				block += 1
			for k in range(len(col_copy)-1, -1, -1):
				if col_copy[k] != 0:
					shift_by = len(col_copy) - k - 1
					break
			# shift list row by shift_by to the right
			col_copy = list(col_copy)
			col_shifted = col_copy[-shift_by:] + col_copy[:-shift_by]

			result = [1 if ((col_copy[i] != 0 and col_shifted[i] != 0) and (col_copy[i] == col_shifted[i])) else 0 for i in range(min(len(col_copy), len(col_shifted)))]
			# where result is 1 make self.assignment[(m, i)] = 1
			for m, value in enumerate(result):
				if value == 1:
					self.assignment[(m, i)] = 1
     
			# simple spaces
			col_groups = [len(list(group)) for key, group in itertools.groupby(result) if key == 1]
			if len(col_groups) == len(self.col_constraints[i]):
				test = [0]*len(result)
				group_fill = 1
				padding_list = []
				for j in range(len(col_groups)):
					padding_list.append(self.col_constraints[i][j] - col_groups[j])
				for k in range(len(col)):
					if result[k] == 1:	
						test[k] = group_fill	
						if k+1 < len(result) and result[k+1] == 0:
							group_fill += 1	
				padded_cells = self.pad_list(test, padding_list)
				print("col", i)
				print("padded_cells", padded_cells)
				# where padded cells are 0 make self.assignment[(m, i)] = 0
				for m, value in enumerate(padded_cells):
					if value == 0:
						self.assignment[(m, i)] = 0


		temp_puzzle = np.zeros((self.n_rows, self.n_cols))
		for key, value in self.assignment.items():
			if value != None:
				temp_puzzle[key] = value
    
		#print(temp_puzzle)
		# forward checking
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
     
		self.all_values = [1,0]
		# make it so where self.assignment is None, it is [0,1]
		for key, value in self.assignment.items():
			if value == None:
				self.assignment[key] = self.all_values
		#print(self.assignment)
	
	def print_assignment(self, assignment):
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				if assignment[(row, col)] == 1:
					print(" #", end="")
				if assignment[(row, col)] == 0:
					print(" .", end="")
				elif assignment[(row, col)] == None:
					print(" x", end="")
			print()
		print()
  
	def pad_list(self, test, padding_list):
		result = [0] * len(test)
		for i, num in enumerate(test):
			if num != 0:
				padding = padding_list[num - 1]
				for j in range(-padding, padding + 1):
					pos = i + j
					if 0 <= pos < len(test):
						result[pos] = num
		return result
 
	def is_consistent(self, puzzle, assignment_temp):
		#row sums and groups
		for i, row in enumerate(puzzle):
			sum_row = np.sum(row)
			row_groups = super().count_groups(row)
				
			if sum_row > self.row_sums[i]:
				return False
			if sum_row == self.row_sums[i] and row_groups != self.row_groups[i]:
				return False
			# count number of None in assignment_temp for this row
			none_count = 0
			for j in range(self.n_cols):
				if assignment_temp[(i, j)] == self.all_values:
					none_count += 1
			if sum_row + none_count < self.row_sums[i]:
				return False
			if none_count == 0:
				if not super().is_valid_row(row, i):
					return False
			#if row_groups > self.row_groups[i]:
			#	return False
				 

		#column sums and groups
		for i, col in enumerate(puzzle.T):
			sum_col = np.sum(col)
			col_groups = super().count_groups(col)
			if sum_col > self.col_sums[i]:
				return False
			if sum_col == self.col_sums[i] and col_groups != self.col_groups[i]:
				return False
			none_count = 0
			for j in range(self.n_rows):
				if assignment_temp[(j, i)] == self.all_values:
					none_count += 1
			if sum_col + none_count < self.col_sums[i]:
				return False
			if none_count == 0:
				if not super().is_valid_col(col, i):
					return False
			#if col_groups > self.col_groups[i]:
			#	return False
		return True

	def start_search(self, puzzle):
		# where dictionary is not None assign values to puzzle
		for key, value in self.assignment.items():
			if value != None:
				puzzle[key] = value
		print("before starting search:")
		self.print_assignment(self.assignment)
		print("------------------------")
		return self.backtracking_search(puzzle)


	def forward_checking(self, puzzle, assignment_temp):
    	# forward checking
		for i, row in enumerate(puzzle):
			if np.sum(row) == self.row_sums[i] and super().count_groups(row) == self.row_groups[i]:
				# assign values from puzzle row to assignment_temp
				for j, value in enumerate(row):
					assignment_temp[(i, j)] = value
		for i, col in enumerate(puzzle.T):
			if np.sum(col) == self.col_sums[i] and super().count_groups(col) == self.col_groups[i]:
				# assign values from puzzle col to assignment_temp
				for j, value in enumerate(col):
					assignment_temp[(j, i)] = value
		return assignment_temp

	def backtracking_search(self, puzzle):
		# if assignment is complete then return assignment
		if self.all_values not in self.assignment.values():
			if super().is_valid(puzzle):
				return self.assignment
			#print("invalid solution, backtracking...")
			return False

  		# select unassigned variable
		# current_cell = position
		# select next key in dictionary which has a value of None
		for key, value in self.assignment.items():
			if value == self.all_values:
				current_cell = key
				#print("current cell = ", current_cell)
				break
		# pick a random cell in self.assignment which has a value of None
		#current_cell = random.choice([key for key, value in self.assignment.items() if value == None])

		self.states_visited += 1

		if self.states_visited % 1 == 0:
			self.print_assignment(self.assignment)
			print("states visited: ", self.states_visited)
			print("current cell = ", current_cell)
			print("\n\n")

		assignment_temp = self.assignment.copy()
  

		# Order domain values
		values_list = [1, 0]
		#random.shuffle(values_list)
		#alues_list = random.choices([[1, 0], [0, 1]], weights=[0.85, 0.15])[0]
		for i in values_list:
			temp_puzzle = puzzle.copy()
			temp_puzzle[current_cell] = i
			assignment_temp[current_cell] = i
			if self.is_consistent(temp_puzzle, assignment_temp):
				self.assignment[current_cell] = i
				inference = self.forward_checking(temp_puzzle, assignment_temp)
				result = self.backtracking_search(temp_puzzle)
				if result != False:
					return result
				self.assignment[current_cell] = self.all_values
		#print("backtracking...")
		return False


def test_solver(solver, row_constraints, col_constraints):
	puzzle = np.zeros((len(row_constraints), len(col_constraints)))
	start_time = time.time()	
	current_solver = solver(puzzle, row_constraints, col_constraints)
	assignments = current_solver.start_search(puzzle)
	end = time.time()
	print(f"Time taken = {end - start_time} s")
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
 
	#row_constraints = [[3], [2,1], [2,2], [1], [2]]
	#col_constraints = [[4], [3,1], [1],   [3], [1]]
 
	#row_constraints = [[7], [1,1,2], [1,1,1,1], [1,2,1], [1,1,1,1], [1,1,2], [7]]
	#col_constraints = [[7], [1,1], [7], [1,1,1], [1,1,1,1], [2,2], [7]]	
	
	#row_constraints = [[4,2], [2], [2,4], [1,2], [7], [3,2], [1,3,2], [2,3], [3,2], [3,2]]
	#col_constraints = [[2], [1,1], [3], [3,1], [1,6], [6], [1,8], [1,1,1], [5,2], [5,2]]

	#row_constraints = [[1, 5, 11, 4] ,[3, 3, 9, 2, 1] ,[2, 8, 5, 5] ,[2, 14, 5] ,[2, 4, 4, 2, 6] ,[2, 6, 5, 2] ,
    #                        [11, 7]  ,[6, 3, 3, 6] ,[1, 7, 5, 5] ,[8, 7, 4]  ,[8, 9, 4] , [12, 1, 8] ,[2, 1, 2], [9, 3], 
    #                         [2], [9], [6], [6], [6], [7], [8], [8], [8], [7], [7]]
	#col_constraints = [[5,6,4],[7,3,5],[2,7,5],[1,6,6],[1,3,6,6],[1,3,6,7],[7,4,7],[11,6],[4,4,1,4],[1,6,1,3],[7,4,3],[6,5,2],[2,2,3,1,2],[4,4,1,1],[4,7,2],
    #                     [4,4,1,2],[5,3,1,1],[6,5,1], [2,2,4,1],[5,1,1],[7,1,1,1],[12,1,1],[5,6,3],[1,10,1],[3,8]]

	#row_constraints = [[4,5],[3,3],[1,3,2],[10],[10],[7,7],[6,3,1],[6,2],[4,1],[3],[1],[3],[1,5],[2,8],[4,8]]
	#col_constraints = [[3,1],[3,2],[1,5,3],[3,5,1],[2,5],[2,6],[3],[3,4],[4,4],[5,4],[1,6,1,3],[1,5,3],[2,3,2],[7,2],[6,2]]


	#test_solver(BF, row_constraints, col_constraints)
	test_solver(backtracking_with_prechecking, row_constraints, col_constraints)



	

	
	

