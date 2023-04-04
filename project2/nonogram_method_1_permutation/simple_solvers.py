import itertools
import time
from main_permutations import nonogram_solver_perm


class brute_force(nonogram_solver_perm):
    def __init__(self, row_constraints, col_constraints):
        super().__init__(row_constraints, col_constraints)
        self.states_visited = 0
    
    def solve(self, puzzle = 0, row_idx=0):            
        if row_idx == len(puzzle):
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None

        for row_permutation in itertools.product([0, 1], repeat=len(puzzle[row_idx])):
            # newest permutation is inserted into the puzzle
            # then it is checked if it is a solution
            new_puzzle = puzzle[:row_idx] + [row_permutation] + puzzle[row_idx+1:]
            self.states_visited += 1  # Increment the states_visited counter
            solution = self.solve(new_puzzle, row_idx + 1)
            if solution is not None:
                return solution

        return None

# simple row sum constraint
class s_row(nonogram_solver_perm):
    def __init__(self, row_constraints, col_constraints):
        super().__init__(row_constraints, col_constraints)
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.rows = len(row_constraints)
        self.cols = len(col_constraints)
        self.row_sums = [sum(row) for row in row_constraints]
        self.states_visited = 0
    
    def row_sum_constraint(self, row_permutation, row_idx):
        if sum(row_permutation) != self.row_sums[row_idx]:
            return True
        return False
    
    
    def solve(self, puzzle = 0, row_idx=0):            
        if row_idx == len(puzzle):
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None

        for row_permutation in itertools.product([0, 1], repeat=len(puzzle[row_idx])):
            # if sum of row_permutation is not equal to sum of row_constraints
            # then continue to next row_permutation
            if self.row_sum_constraint(row_permutation, row_idx):
                continue	
            new_puzzle = puzzle[:row_idx] + [row_permutation] + puzzle[row_idx+1:]
            self.states_visited += 1  # Increment the states_visited counter
            solution = self.solve(new_puzzle, row_idx + 1)
            if solution is not None:
                return solution

        return None

# simple row and column sum constraint
class s_row_col(nonogram_solver_perm):
    def __init__(self, row_constraints, col_constraints):
        super().__init__(row_constraints, col_constraints)
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.rows = len(row_constraints)
        self.cols = len(col_constraints)
        
        self.row_sums = [sum(row) for row in row_constraints]
        self.constraint_sums = [sum(constraint) for constraint in self.col_constraints]
        
        self.states_visited = 0
    
    
    def row_sum_constraint(self, row_permutation, row_idx):
        if sum(row_permutation) != self.row_sums[row_idx]:
            return True
        return False
    
    
    def solve(self, puzzle = 0, row_idx=0):            
        if row_idx == len(puzzle):
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None

        for row_permutation in itertools.product([0, 1], repeat=len(puzzle[row_idx])):
            # if sum of row_permutation is not equal to sum of row_constraints
            # then continue to next row_permutation
            if self.row_sum_constraint(row_permutation, row_idx):
                continue
            
            new_puzzle = puzzle[:row_idx] + [row_permutation] + puzzle[row_idx+1:]

            # Check if the sum of any column in new_puzzle is greater than its constraint sum
            col_sums = [sum(col) for col in zip(*new_puzzle)]
            if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
                continue
            
            
            
            self.states_visited += 1  # Increment the states_visited counter
            # every 1000 states visited, print the current state
            #if self.states_visited % 1000 == 0:
            #    #super().print_current_state(new_puzzle)
            #    print(self.states_visited)
            solution = self.solve(new_puzzle, row_idx + 1)
            if solution is not None:
                return solution

        return None

# simple row and column sum constraint
# and also row and column group constraint
# (checking number of "groups" of filled cells)
class s_row_col_groups(nonogram_solver_perm):
    def __init__(self, row_constraints, col_constraints):
        super().__init__(row_constraints, col_constraints)
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.rows = len(row_constraints)
        self.cols = len(col_constraints)
        
        self.row_sums = [sum(row) for row in row_constraints]
        self.constraint_sums = [sum(constraint) for constraint in self.col_constraints]
        
        
        self.states_visited = 0
    
    def row_sum_constraint(self, row_permutation, row_idx):
        if sum(row_permutation) != self.row_sums[row_idx]:
            return True
        return False
    
    def row_group_constraint(self, row_permutation, row_idx):
        row_groups = [len(list(group)) for key, group in itertools.groupby(row_permutation) if key == 1]
        if len(row_groups) > len(self.row_constraints[row_idx]):
            return True
        return False
    
    def solve(self, puzzle = 0, row_idx=0):            
        if row_idx == len(puzzle):
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None
            
        for row_permutation in itertools.product([0, 1], repeat=len(puzzle[row_idx])):
            # if sum of row_permutation is not equal to sum of row_constraints
            # then continue to next row_permutation
            if self.row_sum_constraint(row_permutation, row_idx):
                continue
            
            if self.row_group_constraint(row_permutation, row_idx):
                continue
            new_puzzle = puzzle[:row_idx] + [row_permutation] + puzzle[row_idx+1:]

            # Check if the sum of any column in new_puzzle is greater than its constraint sum
            col_sums = [sum(col) for col in zip(*new_puzzle)]
            if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
                continue
            
            # Check if the number of groups in any column is greater than the column constraint length
            if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
                continue

            
            self.states_visited += 1  # Increment the states_visited counter
            # every 1000 states visited, print the current state
            #if self.states_visited % 1000 == 0:
                #super().print_current_state(new_puzzle)
                #print(self.states_visited)
            solution = self.solve(new_puzzle, row_idx + 1)
            if solution is not None:
                return solution

        return None

# same as above but not much changed (ignore this)
class s_row_and_col_and_group_o(nonogram_solver_perm):
    def __init__(self, row_constraints, col_constraints):
        super().__init__(row_constraints, col_constraints)
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.rows = len(row_constraints)
        self.cols = len(col_constraints)
        
        self.row_sums = [sum(row) for row in row_constraints]
        self.constraint_sums = [sum(constraint) for constraint in self.col_constraints]
        
        self.row_permutations = list(itertools.product([0, 1], repeat=self.cols))
        
        self.all_row_permutations = [self.row_permutations[:] for _ in range(self.rows)]
        
        self.states_visited = 0
        
        
        # reduce domain of variables before starting search
        # apply constraints to row_permutations
        # if sum of a row_permutation is not equal to the constraint row sum then it is removed
        # if the number of groups in a row_permutation is not equal to the number of groups in the constraint then it is removed
        for i in range(self.rows):
            new_row_permutations = []
            for j in range(len(self.row_permutations)):
                row_groups = [len(list(group)) for key, group in itertools.groupby(self.row_permutations[j]) if key == 1]
                if (sum(self.row_permutations[j]) != self.row_sums[i]) or (len(row_groups) != len(self.row_constraints[i])):
                    pass
                else:
                    new_row_permutations.append(self.row_permutations[j])
                    #continue

            self.all_row_permutations[i] = new_row_permutations
    
    def solve(self, puzzle, row_idx=0):            
        if row_idx == len(puzzle):
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None
            
        for row_permutation in self.all_row_permutations[row_idx]:
            new_puzzle = puzzle[:row_idx] + [row_permutation] + puzzle[row_idx+1:]

            # Check if the sum of any column in new_puzzle is greater than its constraint sum
            col_sums = [sum(col) for col in zip(*new_puzzle)]
            if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
                continue
            
            # Check if the number of groups in any column is greater than the column constraint length
            if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
                continue

            self.states_visited += 1  # Increment the states_visited counter
            # every 1000 states visited, print the current state
            #if self.states_visited % 1000 == 0:
            #    super().print_current_state(new_puzzle)
            #    print(self.states_visited)
            solution = self.solve(new_puzzle, row_idx + 1)
            if solution is not None:
                return solution

        return None