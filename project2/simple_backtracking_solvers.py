import itertools
import time
from nonogram import nonogram_solver


# following backtracking pseudocode from textbook
class A(nonogram_solver):
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

    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in range(self.rows):
            if i not in self.assignment:
                return i
        return None

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

# backtracking + minimum remaining values
class A_MRV(nonogram_solver):
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
            
        self.row_indices_sorted_by_domain = sorted(range(self.rows), key=lambda i: len(self.all_row_permutations[i]))
        for i in self.all_row_permutations:
            print(i)
        print(self.row_indices_sorted_by_domain)


    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in self.row_indices_sorted_by_domain:
            if i not in self.assignment:
                return i
        return None




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

            #if any(len([len(list(group)) for key, group in itertools.groupby(col) if key == 1]) > len(self.col_constraints[c]) for c, col in enumerate(zip(*new_puzzle))):
            #    continue

            # add {var = value} to assignment
            self.assignment[row_idx] = row_permutation
            self.states_visited += 1

            #if self.states_visited % 1000 == 0:
            #    super().print_current_state(new_puzzle)
            
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

# backtracking + least constraining value
class A_LCV(nonogram_solver):
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

    
    def enforce_arc_consistency(self):
        queue = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) not in self.assignment:
                    queue.append((i,j))

        while queue:
            row_idx, col_idx = queue.pop(0)
            row_permutations = self.all_row_permutations[row_idx]
            new_row_permutations = []

            for row_permutation in row_permutations:
                new_puzzle = [self.assignment.get(i, (0,) * self.cols) for i in range(self.rows)]
                new_puzzle[row_idx] = row_permutation
                col = [new_puzzle[r][col_idx] for r in range(self.rows)]
                if all(any(col[c:c+constraint] == [1]*constraint for c in range(self.cols-constraint+1)) for constraint in self.col_constraints[col_idx]):
                    new_row_permutations.append(row_permutation)

            if len(new_row_permutations) != len(row_permutations):
                self.all_row_permutations[row_idx] = new_row_permutations
                for r in range(self.rows):
                    if r != row_idx and (r,col_idx) not in queue:
                        queue.append((r,col_idx))
    
    
    # function SELECT-UNASSIGNED-VARIABLE(csp, assignment) returns a variable
    def select_unassigned_variable(self):
        for i in range(self.rows):
            if i not in self.assignment:
                return i
        return None

    # function BACKTRACK(csp, assignment) returns a solution or failure
    def solve(self, puzzle = 0):
        self.enforce_arc_consistency()
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