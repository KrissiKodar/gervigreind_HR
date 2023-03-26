import itertools
import time
from nonogram_permutations import nonogram_solver_perm


# backtracking and AC3 solvers
class AC3(nonogram_solver_perm):
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

        
        self.assignment = {}
        self.states_visited = 0
        
        # Preprocessing stage: apply constraints to row_permutations
        for i in range(self.rows):
            new_row_permutations = []
            for j in range(len(self.row_permutations)):
                row_groups = [len(list(group)) for key, group in itertools.groupby(self.row_permutations[j]) if key == 1]
                if (sum(self.row_permutations[j]) != self.row_sums[i]) or (len(row_groups) != len(self.row_constraints[i])):
                    pass
                else:
                    new_row_permutations.append(self.row_permutations[j])

            self.all_row_permutations[i] = new_row_permutations
        
        self.col_permutations = list(itertools.product([0, 1], repeat=self.rows))
        self.all_col_permutations = [self.col_permutations[:] for _ in range(self.cols)]

        # Preprocessing stage: apply constraints to col_permutations
        for i in range(self.cols):
            new_col_permutations = []
            for j in range(len(self.col_permutations)):
                col_groups = [len(list(group)) for key, group in itertools.groupby(self.col_permutations[j]) if key == 1]
                if (sum(self.col_permutations[j]) != self.constraint_sums[i]) or (len(col_groups) != len(self.col_constraints[i])):
                    pass
                else:
                    new_col_permutations.append(self.col_permutations[j])

            self.all_col_permutations[i] = new_col_permutations       
            

        self.queue = self.initialize_queue()
        #for i in self.all_row_permutations:
        #    print(len(i))
        if not self.propagate_constraints():
            raise ValueError("No solution exists for the given constraints.")
        #print("\n\n\n")
        #for i in self.all_row_permutations:
        #    print(len(i))

    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in range(self.rows):
            if i not in self.assignment:
                return i
        return None
    
    def initialize_queue(self):
        queue = []
        for row in range(self.rows):
            for col in range(self.cols):
                queue.append((row, col))
        return queue
    
    def propagate_constraints(self):
        while self.queue:
            row, col = self.queue.pop(0)
            if self.revise(row, col):
                if not self.all_row_permutations[row]:
                    return False

                for neighbor in self.neighbors(row, col):
                    self.queue.append(neighbor)

        return True
    
    def revise(self, row, col):
        revised = False

        for row_permutation in self.all_row_permutations[row]:
            consistent = False

            for col_permutation in self.all_col_permutations[col]:
                if row_permutation[col] == col_permutation[row]:
                    consistent = True
                    break

            if not consistent:
                self.all_row_permutations[row].remove(row_permutation)
                revised = True

        return revised
    
    def neighbors(self, row, col):
        neighbors = [(r, col) for r in range(self.rows) if r != row]
        neighbors.extend([(row, c) for c in range(self.cols) if c != col])
        return neighbors
    
    # function BACKTRACK(csp, assignment) returns a solution or failure
    def solve(self, puzzle = 0):
        # var ← SELECT-UNASSIGNED-VARIABLE(csp, assignment)
        row_idx = self.select_unassigned_variable()

        # if assignment is complete then return assignment
        if row_idx is None:
            puzzle = [self.assignment[i] for i in sorted(self.assignment)]
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None

        # for each value in ORDER-DOMAIN-VALUES(csp, var, assignment) do
        for row_permutation in self.all_row_permutations[row_idx]:
            new_puzzle = [self.assignment.get(i, (0,) * self.cols) for i in range(self.rows)]
            new_puzzle[row_idx] = row_permutation

            # if value is not consistent with assignment then
            col_sums = [sum(col) for col in zip(*new_puzzle)]
            if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
                continue

            if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
                continue

            # add {var = value} to assignment
            self.assignment[row_idx] = row_permutation
            self.states_visited += 1

            # inferences ← INFERENCE(csp, var, assignment)
            # (In this implementation, we don't make any specific inferences)
            
            # if inferences ≠ failure then
            # add inferences to csp
            # result ← BACKTRACK(csp, assignment)
            solution = self.solve()

            # if result ≠ failure then return result
            if solution is not None:
                return solution
            else:
                # remove {var = value} from assignment
                del self.assignment[row_idx]
        # return failure
        return None

class AC3_organized(nonogram_solver_perm):
    def __init__(self, row_constraints, col_constraints):
        super().__init__(row_constraints, col_constraints)
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.rows = len(row_constraints)
        self.cols = len(col_constraints)
        print("test1")
        self.row_sums = [sum(row) for row in row_constraints]
        self.constraint_sums = [sum(constraint) for constraint in self.col_constraints]
        print("test2")
        self.row_permutations = list(itertools.product([0, 1], repeat=self.cols))
        print("test3")
        self.all_row_permutations = [self.row_permutations[:] for _ in range(self.rows)]

        print("test4")
        self.assignment = {}
        self.states_visited = 0
        print("test5")
        # Preprocessing stage: apply constraints to row_permutations
        for i in range(self.rows):
            new_row_permutations = []
            for j in range(len(self.row_permutations)):
                row_groups = [len(list(group)) for key, group in itertools.groupby(self.row_permutations[j]) if key == 1]
                if (sum(self.row_permutations[j]) != self.row_sums[i]) or (len(row_groups) != len(self.row_constraints[i])):
                    pass
                else:
                    new_row_permutations.append(self.row_permutations[j])

            self.all_row_permutations[i] = new_row_permutations
        print("test6")
        self.col_permutations = list(itertools.product([0, 1], repeat=self.rows))
        self.all_col_permutations = [self.col_permutations[:] for _ in range(self.cols)]
        print("test7")
        # Preprocessing stage: apply constraints to col_permutations
        for i in range(self.cols):
            new_col_permutations = []
            for j in range(len(self.col_permutations)):
                col_groups = [len(list(group)) for key, group in itertools.groupby(self.col_permutations[j]) if key == 1]
                if (sum(self.col_permutations[j]) != self.constraint_sums[i]) or (len(col_groups) != len(self.col_constraints[i])):
                    pass
                else:
                    new_col_permutations.append(self.col_permutations[j])

            self.all_col_permutations[i] = new_col_permutations       
            
        print("test8")
        self.queue = self.initialize_queue()
        #for i in self.all_row_permutations:
        #    print(len(i))
        if not self.propagate_constraints():
            raise ValueError("No solution exists for the given constraints.")
        if True:
            print("\n\n\n")
            self.state_space_after_reduction = 1
            for i in self.all_row_permutations:
                print(len(i))
                self.state_space_after_reduction *= len(i) 
            
            self.state_space_before = 2**(self.rows * self.cols)
            print("State space before AC3: " + str('{:.2e}'.format(self.state_space_before)))
            print("State space after AC3: " + str('{:.2e}'.format(self.state_space_after_reduction)))
            print("State space reduced factor: " + str('{:.2e}'.format(self.state_space_after_reduction / self.state_space_before)))

        
    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in range(self.rows):
            if i not in self.assignment:
                return i
        return None
    
    def initialize_queue(self):
        queue = []
        for row in range(self.rows):
            for col in range(self.cols):
                queue.append((row, col))
        return queue
    
    def propagate_constraints(self):
        while self.queue:
            row, col = self.queue.pop(0)

            if self.revise(row, col):
                if not self.all_row_permutations[row]:
                    return False

                for neighbor in self.neighbors(row, col):
                    self.queue.append(neighbor)

        return True
    
    def revise(self, row, col):
        revised = False

        for row_permutation in self.all_row_permutations[row]:
            consistent = False

            for col_permutation in self.all_col_permutations[col]:
                if row_permutation[col] == col_permutation[row]:
                    consistent = True
                    break

            if not consistent:
                self.all_row_permutations[row].remove(row_permutation)
                revised = True

        return revised
    
    def neighbors(self, row, col):
        neighbors = [(r, col) for r in range(self.rows) if r != row]
        neighbors.extend([(row, c) for c in range(self.cols) if c != col])
        return neighbors  
    
    def check_if_consistent(self, row_idx, row_permutation):
        new_puzzle = [self.assignment.get(i, (0,) * self.cols) for i in range(self.rows)]
        new_puzzle[row_idx] = row_permutation
        col_sums = [sum(col) for col in zip(*new_puzzle)]
        super().print_current_state(new_puzzle)
        if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
            return False
        if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
            return False
        return True
    
    def solve(self, puzzle = 0):
        row_idx = self.select_unassigned_variable()

        if row_idx is None:
            puzzle = [self.assignment[i] for i in sorted(self.assignment)]
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None

        for row_permutation in self.all_row_permutations[row_idx]:
            if not self.check_if_consistent(row_idx, row_permutation):
                continue

            self.assignment[row_idx] = row_permutation
            self.states_visited += 1
            
            solution = self.solve()

            if solution is not None:
                return solution
            else:
                del self.assignment[row_idx]
        return None

    def fraction_of_states_visited(self):
        return self.states_visited / self.state_space_after_reduction

class AC3_backjumping(nonogram_solver_perm):
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

        
        self.assignment = {}
        self.states_visited = 0
        
        # Preprocessing stage: apply constraints to row_permutations
        for i in range(self.rows):
            new_row_permutations = []
            for j in range(len(self.row_permutations)):
                row_groups = [len(list(group)) for key, group in itertools.groupby(self.row_permutations[j]) if key == 1]
                if (sum(self.row_permutations[j]) != self.row_sums[i]) or (len(row_groups) != len(self.row_constraints[i])):
                    pass
                else:
                    new_row_permutations.append(self.row_permutations[j])

            self.all_row_permutations[i] = new_row_permutations
        
        self.col_permutations = list(itertools.product([0, 1], repeat=self.rows))
        self.all_col_permutations = [self.col_permutations[:] for _ in range(self.cols)]

        # Preprocessing stage: apply constraints to col_permutations
        for i in range(self.cols):
            new_col_permutations = []
            for j in range(len(self.col_permutations)):
                col_groups = [len(list(group)) for key, group in itertools.groupby(self.col_permutations[j]) if key == 1]
                if (sum(self.col_permutations[j]) != self.constraint_sums[i]) or (len(col_groups) != len(self.col_constraints[i])):
                    pass
                else:
                    new_col_permutations.append(self.col_permutations[j])

            self.all_col_permutations[i] = new_col_permutations       
            

        self.queue = self.initialize_queue()
        #for i in self.all_row_permutations:
        #    print(len(i))
        if not self.propagate_constraints():
            raise ValueError("No solution exists for the given constraints.")
        #print("\n\n\n")
        #for i in self.all_row_permutations:
        #    print(len(i))

        
    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in range(self.rows):
            if i not in self.assignment:
                return i
        return None
    
    def initialize_queue(self):
        queue = []
        for row in range(self.rows):
            for col in range(self.cols):
                queue.append((row, col))
        return queue
    
    def propagate_constraints(self):
        while self.queue:
            row, col = self.queue.pop(0)

            if self.revise(row, col):
                if not self.all_row_permutations[row]:
                    return False

                for neighbor in self.neighbors(row, col):
                    self.queue.append(neighbor)

        return True
    
    def revise(self, row, col):
        revised = False

        for row_permutation in self.all_row_permutations[row]:
            consistent = False

            for col_permutation in self.all_col_permutations[col]:
                if row_permutation[col] == col_permutation[row]:
                    consistent = True
                    break

            if not consistent:
                self.all_row_permutations[row].remove(row_permutation)
                revised = True

        return revised
    
    def neighbors(self, row, col):
        neighbors = [(r, col) for r in range(self.rows) if r != row]
        neighbors.extend([(row, c) for c in range(self.cols) if c != col])
        return neighbors  
    
    def check_if_consistent(self, row_idx, row_permutation):
        new_puzzle = [self.assignment.get(i, (0,) * self.cols) for i in range(self.rows)]
        new_puzzle[row_idx] = row_permutation
        col_sums = [sum(col) for col in zip(*new_puzzle)]
        
        if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
            return False
        if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
            return False
        return True
    
    def find_conflict_set(self, row_idx, row_permutation):
        conflict_set = set()
        new_puzzle = [self.assignment.get(i, (0,) * self.cols) for i in range(self.rows)]
        new_puzzle[row_idx] = row_permutation
        col_sums = [sum(col) for col in zip(*new_puzzle)]

        for col_idx, (col_sum, constraint_sum) in enumerate(zip(col_sums, self.constraint_sums)):
            if col_sum > constraint_sum:
                for r in range(row_idx):
                    if self.assignment.get(r, (0,) * self.cols)[col_idx] == 1:
                        conflict_set.add(r)

        for col_idx, col in enumerate(zip(*new_puzzle)):
            if len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[col_idx]):
                for r in range(row_idx):
                    if self.assignment.get(r, (0,) * self.cols)[col_idx] == 1:
                        conflict_set.add(r)

        return conflict_set

    def backjumping_solve(self):
        row_idx = self.select_unassigned_variable()
        if row_idx is None:
            puzzle = [self.assignment[i] for i in sorted(self.assignment)]
            if super().is_valid(puzzle):
                return puzzle, None
            else:
                return None, None

        conflict_set = None  # Initialize conflict_set before the loop
        for row_permutation in self.all_row_permutations[row_idx]:
            if not self.check_if_consistent(row_idx, row_permutation):
                continue

            self.assignment[row_idx] = row_permutation
            self.states_visited += 1

            solution, conflict_set = self.backjumping_solve()

            if solution is not None:
                return solution, None
            else:
                del self.assignment[row_idx]
                if conflict_set is not None:
                    conflict_set.add(row_idx)
                else:
                    conflict_set = self.find_conflict_set(row_idx, row_permutation)
                    conflict_set.add(row_idx)

        return None, conflict_set

    def solve(self, puzzle=0):
        solution, _ = self.backjumping_solve()
        return solution

class AC3_iterative_deepening(nonogram_solver_perm):
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

        
        self.assignment = {}
        self.states_visited = 0
        
        # Preprocessing stage: apply constraints to row_permutations
        for i in range(self.rows):
            new_row_permutations = []
            for j in range(len(self.row_permutations)):
                row_groups = [len(list(group)) for key, group in itertools.groupby(self.row_permutations[j]) if key == 1]
                if (sum(self.row_permutations[j]) != self.row_sums[i]) or (len(row_groups) != len(self.row_constraints[i])):
                    pass
                else:
                    new_row_permutations.append(self.row_permutations[j])

            self.all_row_permutations[i] = new_row_permutations
        
        self.col_permutations = list(itertools.product([0, 1], repeat=self.rows))
        self.all_col_permutations = [self.col_permutations[:] for _ in range(self.cols)]

        # Preprocessing stage: apply constraints to col_permutations
        for i in range(self.cols):
            new_col_permutations = []
            for j in range(len(self.col_permutations)):
                col_groups = [len(list(group)) for key, group in itertools.groupby(self.col_permutations[j]) if key == 1]
                if (sum(self.col_permutations[j]) != self.constraint_sums[i]) or (len(col_groups) != len(self.col_constraints[i])):
                    pass
                else:
                    new_col_permutations.append(self.col_permutations[j])

            self.all_col_permutations[i] = new_col_permutations       
            

        self.queue = self.initialize_queue()
        #for i in self.all_row_permutations:
        #    print(len(i))
        if not self.propagate_constraints():
            raise ValueError("No solution exists for the given constraints.")
        #print("\n\n\n")
        #for i in self.all_row_permutations:
        #    print(len(i))

        
    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in range(self.rows):
            if i not in self.assignment:
                return i
        return None
    
    def initialize_queue(self):
        queue = []
        for row in range(self.rows):
            for col in range(self.cols):
                queue.append((row, col))
        return queue
    
    def propagate_constraints(self):
        while self.queue:
            row, col = self.queue.pop(0)

            if self.revise(row, col):
                if not self.all_row_permutations[row]:
                    return False

                for neighbor in self.neighbors(row, col):
                    self.queue.append(neighbor)

        return True
    
    def revise(self, row, col):
        revised = False

        for row_permutation in self.all_row_permutations[row]:
            consistent = False

            for col_permutation in self.all_col_permutations[col]:
                if row_permutation[col] == col_permutation[row]:
                    consistent = True
                    break

            if not consistent:
                self.all_row_permutations[row].remove(row_permutation)
                revised = True

        return revised
    
    def neighbors(self, row, col):
        neighbors = [(r, col) for r in range(self.rows) if r != row]
        neighbors.extend([(row, c) for c in range(self.cols) if c != col])
        return neighbors  
    
    def check_if_consistent(self, row_idx, row_permutation):
        new_puzzle = [self.assignment.get(i, (0,) * self.cols) for i in range(self.rows)]
        new_puzzle[row_idx] = row_permutation
        col_sums = [sum(col) for col in zip(*new_puzzle)]
        
        if any(col_sum > constraint_sum for col_sum, constraint_sum in zip(col_sums, self.constraint_sums)):
            return False
        if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
            return False
        return True
    
    def depth_limited_search(self, depth_limit, depth=0):
        row_idx = self.select_unassigned_variable()

        # Return failure when the depth limit is exceeded
        if depth > depth_limit:
            return None

        if row_idx is None:
            puzzle = [self.assignment[i] for i in sorted(self.assignment)]
            if super().is_valid(puzzle):
                return puzzle
            else:
                return None

        for row_permutation in self.all_row_permutations[row_idx]:
            if not self.check_if_consistent(row_idx, row_permutation):
                continue

            self.assignment[row_idx] = row_permutation
            self.states_visited += 1

            solution = self.depth_limited_search(depth_limit, depth + 1)

            if solution is not None:
                return solution
            else:
                del self.assignment[row_idx]
        return None

    def solve(self, puzzle = None):
        depth_limit = 0
        while True:
            solution = self.depth_limited_search(depth_limit)
            if solution is not None:
                return solution
            depth_limit += 1
            #print(f"Depth limit increased to {depth_limit}")
