import numpy as np
import itertools
import time
import random
from ortools.sat.python import cp_model

class ortools_solver:
    def __init__(self, row_constraints, col_constraints):
        self.row_constraints = row_constraints
        self.row_len = len(row_constraints)
        self.row_sums = [np.sum(row) for row in self.row_constraints]
        self.row_groups = [len(row) for row in self.row_constraints]

        self.col_constraints = col_constraints
        self.col_len = len(col_constraints)
        self.col_sums = [np.sum(col) for col in self.col_constraints]
        self.col_groups = [len(col) for col in self.col_constraints]
    
    def count_groups(self, row_or_col):
        count = 0
        prev_elem = 0
        for elem in row_or_col:
            count += elem * (1 - prev_elem)
            prev_elem = elem
        return count
    
    def setup_csp(self):
        model = cp_model.CpModel()
        grid = {}
        for i in range(self.row_len):
            for j in range(self.col_len):
                grid[(i, j)] = model.NewIntVar(0, 1, f"{(i, j)}")

        # Add the sum constraints to the model
        # sum of row constraints == sum of row
        for i in range(self.row_len):
            row_i = [grid[(i, j)] for j in range(self.col_len)]
            model.Add(sum(row_i) == self.row_sums[i])
        # sum of col constraints == sum of col
        for j in range(self.col_len):
            col_j = [grid[(i, j)] for i in range(self.row_len)]
            model.Add(sum(col_j) == self.col_sums[j])

        # Add the section group constraints to the model
        # This is the part which I cannot get to work
        # the error I get is:
        """  Traceback (most recent call last):
            File "c:\repos\gervigreind_HR\project2\ortools_nonogram.py", line 110, in <module>
                ot_nonogram_solver.solve_csp()
            File "c:\repos\gervigreind_HR\project2\ortools_nonogram.py", line 70, in solve_csp
                model, variables = self.setup_csp()
                                ^^^^^^^^^^^^^^^^
            File "c:\repos\gervigreind_HR\project2\ortools_nonogram.py", line 51, in setup_csp
                model.Add(self.count_groups(row_i) == self.row_groups[i])
                        ^^^^^^^^^^^^^^^^^^^^^^^^
            File "c:\repos\gervigreind_HR\project2\ortools_nonogram.py", line 23, in count_groups
                count += elem * (1 - prev_elem)
                        ~~~~~^~~~~~~~~~~~~~~~~
            File "C:\repos\gervigreind_HR\.venv\Lib\site-packages\ortools\sat\python\cp_model.py", line 341, in __mul__
                arg = cmh.assert_is_a_number(arg)
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
            File "C:\repos\gervigreind_HR\.venv\Lib\site-packages\ortools\sat\python\cp_model_helper.py", line 80, in assert_is_a_number
                raise TypeError('Not an number: %s' % x)
            TypeError: Not an number: (-(0, 0) + 1) """
        
        for i in range(self.row_len):
            row_i = [grid[(i, j)] for j in range(self.col_len)]
            print(row_i)
            model.Add(self.count_groups(row_i) == self.row_groups[i])
                
        for j in range(self.col_len):
            col_j = [grid[(i, j)] for i in range(self.row_len)]
            model.Add(self.count_groups(col_j) == self.col_groups[j])
            
            
        return model, grid

    def print_solution(self, grid):
        for i in range(self.row_len):
            for j in range(self.col_len):
                if grid[(i, j)] == 1:
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        print()

    def solve_csp(self):
        # create the model
        model, variables = self.setup_csp()
        # create the solver
        solver = cp_model.CpSolver()
        solution_printer = cp_model.VarArraySolutionPrinter(list(variables.values()))
        # find all solutions and print them out
        status = solver.SearchForAllSolutions(model, solution_printer)
        if status == cp_model.INFEASIBLE:
            print("ERROR: Model does not have a solution!")
        elif status == cp_model.MODEL_INVALID:
            print("ERROR: Model is invalid!")
            model.Validate()
        elif status == cp_model.UNKNOWN:
            print("ERROR: No solution was found!")
        else:
            n = solution_printer.solution_count()
            print("%d solution(s) found." % n)
            print(solver.ResponseStats())
            if n > 1:
                print("ERROR: There should just be one solution!")
            else:
                # Print the solved Nonogram board for each solution
                grid = {}
                for (i, j), var in variables.items():
                    grid[(i, j)] = solver.Value(var)
                self.print_solution(grid, len(row_constraints), len(col_constraints))
    
    def kk(self):
        # create the model
        model, variables = self.setup_csp()
        # create the solver
        solver = cp_model.CpSolver()
        solution_printer = cp_model.VarArraySolutionPrinter(list(variables.values()))
        # find all solutions and print them out
        status = solver.SearchForAllSolutions(model, solution_printer)
        #print(status)

if __name__ == "__main__":
    row_constraints = [[4,2], [2], [2,4], [1,2], [7], [3,2], [1,3,2], [2,3], [3,2], [3,2]]
    col_constraints = [[2], [1,1], [3], [3,1], [1,6], [6], [1,8], [1,1,1], [5,2], [5,2]]
    ot_nonogram_solver = ortools_solver(row_constraints, col_constraints)
    ot_nonogram_solver.solve_csp()