import time
from utility_functions import *

class csp_nonogram:
    def __init__(self, row_constraints, col_constraints):
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        
        self.row_constraint_sums = [sum(i) for i in row_constraints]
        self.col_constraint_sums = [sum(i) for i in col_constraints]

        self.row_constraint_groups = [len(i) for i in row_constraints]
        self.col_constraint_groups = [len(i) for i in col_constraints]

        self.n_rows = len(row_constraints)
        self.n_cols = len(col_constraints)

        self.assignment = {}

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                self.assignment[(i,j)] = None



class nonogram_solver_1:
    def __init__(self, csp):
        # simple boxes
        confirmed_rows = confirmed_filled_in(csp.row_constraints, csp.row_constraint_sums, csp.row_constraint_groups, csp.n_rows)
        confirmed_cols = confirmed_filled_in(csp.col_constraints, csp.col_constraint_sums, csp.col_constraint_groups, csp.n_cols)

        fill_in_confirmed(csp.row_constraints, confirmed_rows, csp.assignment, csp.n_rows, csp.n_cols, 1, True)
        fill_in_confirmed(csp.col_constraints, confirmed_cols, csp.assignment, csp.n_rows, csp.n_cols, 1, False)
        
        # I could not get this to work like in the first attempt
        """ # simple spaces
        cr1, cc1 = simple_spaces(csp, csp.assignment)
        cr2, cc2 = row_and_col_current(csp, csp.assignment)
        print("row constraints", csp.row_constraints)
        print("cr1", cr1)
        print("cr2", cr2)
        print()
        for i in range(csp.n_rows):
            print(f" ROW {i} ")
            print(f"The row = {cr1[i]}")
            filled_indices = get_indices(cr1[i], 1)
            print(f"row {i}, indices of 1: {filled_indices}")
            contiguous_ranges = get_contiguous_ranges(filled_indices)
            print(f"row {i}, contiguous ranges: {contiguous_ranges}")
            if len(cr2[i]) == len(row_constraints[i]):
                print("DOING IT")
                padding = []
                for j in range(len(cr2[i])):
                    padding.append(row_constraints[i][j] - cr2[i][j])
                print(f"row {i}, group {j}, padding {padding}")
                ss_row = pad_a_list(cr1[i], contiguous_ranges, padding)
                print(f"row {i}, ss_row {ss_row}")
                # where ss_row is 0, fill in 0 in assignment
                for j in range(len(ss_row)):	
                    if ss_row[j] == 0:
                        csp.assignment[(i,j)] = 0 """
        
        print("\n######### assignment before search #########\n")
        print_assignment(csp, csp.assignment)
        print("\n############################################\n")
        
        
        
        
        self.states_visited = 0
        
    def select_unassigned_variable(self, csp, assignment):
        n_rows = csp.n_rows
        n_cols = csp.n_cols
        for i in range(n_rows):
            for j in range(n_cols):
                if assignment[(i,j)] == None:
                    return (i,j)
        return None

    def order_domain_values(self, var, csp, assignment):
        return [1,0]

    def is_consistent(self, var, value, csp, assignment):
        row_constraints = csp.row_constraints
        col_constraints = csp.col_constraints
        
        row_constraint_sums = csp.row_constraint_sums
        col_constraint_sums = csp.col_constraint_sums
        
        row_constraint_groups = csp.row_constraint_groups
        col_constraint_groups = csp.col_constraint_groups
        
        n_rows = csp.n_rows
        n_cols = csp.n_cols
        
        # create copy of assignment
        assignment_c = assignment.copy()
        assignment_c[(var[0], var[1])] = value
        
        sum_rows = sum_assignment_row(assignment_c, n_rows, n_cols)
        sum_cols = sum_assignment_col(assignment_c, n_rows, n_cols)
        
        groups_rows = count_groups_in_rows(assignment_c, n_rows, n_cols)
        groups_cols = count_groups_in_cols(assignment_c, n_rows, n_cols)
        
        unassigned_rows = count_unassigned_in_rows(assignment_c, n_rows, n_cols)
        unassigned_cols = count_unassigned_in_cols(assignment_c, n_rows, n_cols)
        
        for i in range(n_rows):
            if sum_rows[i] > row_constraint_sums[i]:
                return False
        for i in range(n_cols):
            if sum_cols[i] > col_constraint_sums[i]:
                return False
            
        for i in range(n_rows):
            group_check = ((groups_rows[i] != row_constraint_groups[i]) and unassigned_rows[i] == 0)
            sum_check = ((sum_rows[i] != row_constraint_sums[i]) and unassigned_rows[i] == 0)
            if group_check or sum_check:
                return False
        for i in range(n_cols):
            group_check = ((groups_cols[i] != col_constraint_groups[i]) and unassigned_cols[i] == 0)
            sum_check = ((sum_cols[i] != col_constraint_sums[i]) and unassigned_cols[i] == 0)
            if group_check or sum_check:
                return False
        
        return True
        
    def backtrack(self, csp, assignment):
        # if None is not in assignment.values():
        if None not in assignment.values():
            return assignment
        self.states_visited += 1
        var = self.select_unassigned_variable(csp, assignment)
        for value in self.order_domain_values(var, csp, assignment):
            if self.is_consistent(var, value, csp, assignment):
                assignment[var] = value
                result = self.backtrack(csp, assignment)
                if result != None:
                    return result
                assignment[var] = None
        return None

    def backtracking_search(self, csp):
        return self.backtrack(csp, csp.assignment)


def test_solver(csp, solver):
    start_time = time.time()
    solution = solver.backtracking_search(csp)
    end_time = time.time()
    if solution != None:
        print("Solution found!")
        print_assignment(csp, solver.backtracking_search(csp))
        print("Time to solve: ", end_time - start_time)
        print("States visited: ", solver.states_visited)
    else:
        print("No solution found")





# I could not get the prechecking to work as well as in the nonogram_method_2 folder
# so this solver can only solve small puzzles (not the 10x10 puzzle)


row_constraints = [[3], [2,1], [2,2], [1], [2]]
col_constraints = [[4], [3,1], [1],   [3], [1]]
#row_constraints = [[4,2], [2], [2,4], [1,2], [7], [3,2], [1,3,2], [2,3], [3,2], [3,2]]
#col_constraints = [[2], [1,1], [3], [3,1], [1,6], [6], [1,8], [1,1,1], [5,2], [5,2]]
the_csp = csp_nonogram(row_constraints, col_constraints)

solver = nonogram_solver_1(the_csp)


test_solver(the_csp, solver)