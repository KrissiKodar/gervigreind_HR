import itertools
import time
import numpy as np
import matplotlib.pyplot as plt
import re

class nonogram_solver_perm:
    def __init__(self, row_constraints, col_constraints):
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
 
    # this function checks if the current filled in puzzle
    # satisfies the row and column constraints
    # it checks if the puzzle is actually solved, if so return True
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
    
    def print_current_state(self, puzzle):
        print("\n")
        for row in puzzle:
            print("".join(["# " if cell == 1 else "- " for cell in row]))
        print("\n")
    
    def print_states_visited(self, current_solver):
        print("States visited:", current_solver.states_visited)
    
    
    def __str__(self):
        return self.__class__.__name__
    
    def __name__(self):
        return self.__class__.__name__


class nonogram_puzzle_and_constraints:
    def __init__(self, row_constraints, col_constraints):
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.rows = len(row_constraints)
        self.cols = len(col_constraints)

    def __str__(self):
        return f"{self.rows} by {self.cols} puzzle"  
    
    def __name__(self):
        return f"{self.rows} by {self.cols}"
    
    def get_constraints(self):
        return self.row_constraints, self.col_constraints

    def get_puzzle(self):
        return [(0,) * self.cols] * self.rows


def test_solver(solver, puzzle):
    start_time = time.time()
    current_solver = solver(*puzzle.get_constraints())
    solution = current_solver.solve(puzzle.get_puzzle())
    end_time = time.time()
    #print("\n")
    #print(str(puzzle) + " solved with " + str(current_solver))
    if solution is not None:
        #print(f"Time to solve: {end_time - start_time} seconds")
        #current_solver.print_states_visited(current_solver)
        #print("Solution:")
        for row in solution:
            print("".join(["# " if cell == 1 else "- " for cell in row]))
        solution_time = end_time - start_time
        states_explored = current_solver.states_visited
        return solution_time, states_explored, str(current_solver)
    else:
        print("No solution found.")
        current_solver.print_states_visited(current_solver)



def run_solvers_on_puzzles(solvers, puzzles):
    results = {}
    for solver in solvers:
        solver_name = re.search(r'\.?(\w+)\'?>$', str(solver)).group(1)
        results[solver_name] = {'times': [], 'states_visited': []}
        for puzzle in puzzles:
            try:
                solution_time, states_explored, _ = test_solver(solver, puzzle)
                results[solver_name]['times'].append(solution_time)
                results[solver_name]['states_visited'].append(states_explored)
            except Exception as e:
                print(f"Error occurred for solver {solver_name} on puzzle {puzzle}: {e}")
    return results

def plot_metrics(results):
    plt.rcParams.update({'font.size': 8})
    solver_names = list(results.keys())
    avg_times = [np.mean(results[solver]['times']) for solver in solver_names]
    avg_states_visited = [np.mean(results[solver]['states_visited']) for solver in solver_names]

    def create_subplot(title, ylabel, yscale='linear'):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_title(title)
        ax.set_xlabel('Solvers')
        ax.set_ylabel(ylabel)
        ax.set_yscale(yscale)
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        return fig, ax

    # Average Time (Linear)
    fig_time_linear, ax_time_linear = create_subplot('Average Time (Linear)', 'Average Time (s)')
    ax_time_linear.bar(solver_names, avg_times, alpha=0.5, color='b', label='Average Time')
    plt.show()

    # Average Time (Logarithmic)
    fig_time_log, ax_time_log = create_subplot('Average Time (Logarithmic)', 'Average Time (s)', yscale='log')
    ax_time_log.bar(solver_names, avg_times, alpha=0.5, color='b', label='Average Time')
    plt.show()

    # Average States Visited (Linear)
    fig_states_linear, ax_states_linear = create_subplot('Average States Visited (Linear)', 'Average States Visited')
    ax_states_linear.bar(solver_names, avg_states_visited, alpha=0.5, color='g', label='Average States Visited')
    plt.show()

    # Average States Visited (Logarithmic)
    fig_states_log, ax_states_log = create_subplot('Average States Visited (Logarithmic)', 'Average States Visited', yscale='log')
    ax_states_log.bar(solver_names, avg_states_visited, alpha=0.5, color='g', label='Average States Visited')
    plt.show()



from simple_solvers import *
from simple_backtracking_solvers import *
from AC3_solvers import *


# if name main
if __name__ == "__main__":	
    col_constraints_5_by_5 =   [[4], [3,1], [1], [3], [1]]
    row_constraints_5_by_5= [[3],[2,1], [2,2],[1],[2]]

    puzzle_5_by_5 = nonogram_puzzle_and_constraints(row_constraints_5_by_5, col_constraints_5_by_5)


    col_constraints_7_by_7 = [[7], [1,1], [7], [1,1,1], [1,1,1,1], [2,2], [7]]
    row_constraints_7_by_7 = [[7], [1,1,2], [1,1,1,1], [1,2,1], [1,1,1,1], [1,1,2], [7]]

    puzzle_7_by_7 = nonogram_puzzle_and_constraints(row_constraints_7_by_7, col_constraints_7_by_7)

    col_constraints_10_by_10 = [[2], [1,1], [3], [3,1], [1,6], [6], [1,8], [1,1,1], [5,2], [5,2]]
    row_constraints_10_by_10 = [[4,2], [2], [2,4], [1,2], [7], [3,2], [1,3,2], [2,3], [3,2], [3,2]]
    puzzle_10_by_10 = nonogram_puzzle_and_constraints(row_constraints_10_by_10, col_constraints_10_by_10)
    
    col_constraints_10_by_10_2 = [[4,2], [3], [4], [2], [5], [1,1], [1,6], [6,1], [8,1], [4,1]]
    row_constraints_10_by_10_2 = [[2], [3,2], [3,4], [3,3], [1,1,3], [6], [2,3], [1,1,3], [1,1,1], [6]]
    puzzle_10_by_10_2 = nonogram_puzzle_and_constraints(row_constraints_10_by_10_2, col_constraints_10_by_10_2)

    col_constraints_house = [[5,6,4],[7,3,5],[2,7,5],[1,6,6],[1,3,6,6],[1,3,6,7],[7,4,7],[11,6],[4,4,1,4],[1,6,1,3],[7,4,3],[6,5,2],[2,2,3,1,2],[4,4,1,1],[4,7,2],
                         [4,4,1,2],[5,3,1,1],[6,5,1], [2,2,4,1],[5,1,1],[7,1,1,1],[12,1,1],[5,6,3],[1,10,1],[3,8]]

    row_constraints_house = [[1, 5, 11, 4] ,[3, 3, 9, 2, 1] ,[2, 8, 5, 5] ,[2, 14, 5] ,[2, 4, 4, 2, 6] ,[2, 6, 5, 2] ,
                            [11, 7]  ,[6, 3, 3, 6] ,[1, 7, 5, 5] ,[8, 7, 4]  ,[8, 9, 4] , [12, 1, 8] ,[2, 1, 2], [9, 3], 
                             [2], [9], [6], [6], [6], [7], [8], [8], [8], [7], [7]]
    puzzle_house = nonogram_puzzle_and_constraints(row_constraints_house, col_constraints_house)
    #test_solver(brute_force, puzzle_5_by_5)
    # list of solver 
    # s_row_constraint, s_row_and_col, s_row_and_col_and_group, s_row_and_col_and_group_o, AC3, AC3_iterative_deepening, A
    #list_of_solvers = [brute_force, s_row, s_row_col, s_row_col_groups, AC3_organized, AC3_backjumping]
    
    list_of_solvers = [s_row_col_groups, AC3_organized, AC3_backjumping]
    list_of_puzzles = [puzzle_10_by_10]
    #test_solver(s_row_col, puzzle_7_by_7)
    # Run the solvers on the puzzles
    #results = run_solvers_on_puzzles(list_of_solvers, list_of_puzzles)

    # Plot the metrics
    #plot_metrics(results)
    
    test_solver(AC3_organized, puzzle_7_by_7)
