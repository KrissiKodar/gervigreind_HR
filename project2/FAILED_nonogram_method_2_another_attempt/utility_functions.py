def sum_assignment_row(assignment, n_rows, n_cols):
    # sum row 1 of assignment, ignore None
    sum_rows = [0]*n_rows
    for i in range(n_rows):
        for j in range(n_cols):
            if assignment[(i,j)] == 1:
                sum_rows[i] += 1
    return sum_rows

def sum_assignment_col(assignment, n_rows, n_cols):
    # sum col 1 of assignment, ignore None
    sum_cols = [0]*n_cols
    for i in range(n_cols):
        for j in range(n_rows):
            if assignment[(j,i)] == 1:
                sum_cols[i] += 1
    return sum_cols


def count_groups_in_rows(assignment, n_rows, n_cols):
    groups = [0]*n_rows
    for i in range(n_rows):
        count = 0
        prev_element = 0
        for j in range(n_cols):
            elem = assignment[(i,j)]
            if elem == None:
                elem = 0
            count += (elem*(1-prev_element))
            prev_element = elem
        groups[i] = count
    return groups

def count_groups_in_cols(assignment, n_rows, n_cols):
    groups = [0]*n_cols
    for i in range(n_cols):
        count = 0
        prev_element = 0
        for j in range(n_rows):
            elem = assignment[(j,i)]
            if elem == None:
                elem = 0
            count += (elem*(1-prev_element))
            prev_element = elem
        groups[i] = count
    return groups
    
def count_unassigned_in_rows(assignment, n_rows, n_cols):
    unassigned = [0]*n_rows
    for i in range(n_rows):
        count = 0
        for j in range(n_cols):
            elem = assignment[(i,j)]
            if elem == None:
                count += 1
        unassigned[i] = count
    return unassigned

def count_unassigned_in_cols(assignment, n_rows, n_cols):
    unassigned = [0]*n_cols
    for i in range(n_cols):
        count = 0
        for j in range(n_rows):
            elem = assignment[(j,i)]
            if elem == None:
                count += 1
        unassigned[i] = count
    return unassigned


# this function checks if the filled out 
# grid is a valid solution
def check_if_valid_solution(csp, assignment):
    row_constraints = csp.row_constraints
    col_constraints = csp.col_constraints
    n_rows = csp.n_rows
    n_cols = csp.n_cols
    # check rows first
    check_rows = []
    check_cols = []
    for i in range(n_rows):
        # count 1's in row from left to right
        # if 0 is encountered, then start counting again
        filled_count = 0
        filled_list= []
        zero_encountered = False
        for j in range(n_cols):
            current_cell = assignment[(i,j)]
            filled_count += current_cell
            if current_cell == 0:
                filled_list.append(filled_count)
                filled_count = 0
            if j == n_cols - 1:
                filled_list.append(filled_count)
        # remove 0's from filled_list
        filled_list = [x for x in filled_list if x != 0]	
        check_rows.append(filled_list)
    for i in range(n_cols):
        # count 1's in row from left to right
        # if 0 is encountered, then start counting again
        filled_count = 0
        filled_list= []
        zero_encountered = False
        for j in range(n_rows):
            current_cell = assignment[(j,i)]
            filled_count += current_cell
            if current_cell == 0:
                filled_list.append(filled_count)
                filled_count = 0
            if j == n_rows - 1:
                filled_list.append(filled_count)
        # remove 0's from filled_list
        filled_list = [x for x in filled_list if x != 0]	
        check_cols.append(filled_list)
    
    return check_rows == row_constraints and check_cols == col_constraints

def row_and_col_current(csp, assignment):
    row_constraints = csp.row_constraints
    col_constraints = csp.col_constraints
    n_rows = csp.n_rows
    n_cols = csp.n_cols
    # check rows first
    check_rows = []
    check_cols = []
    for i in range(n_rows):
        # count 1's in row from left to right
        # if 0 is encountered, then start counting again
        filled_count = 0
        filled_list= []
        zero_encountered = False
        for j in range(n_cols):
            current_cell = assignment[(i,j)]
            if current_cell == None:
                current_cell = 0
            filled_count += current_cell
            if current_cell == 0:
                filled_list.append(filled_count)
                filled_count = 0
            if j == n_cols - 1:
                filled_list.append(filled_count)
        # remove 0's from filled_list
        filled_list = [x for x in filled_list if x != 0]	
        check_rows.append(filled_list)
    for i in range(n_cols):
        # count 1's in row from left to right
        # if 0 is encountered, then start counting again
        filled_count = 0
        filled_list= []
        zero_encountered = False
        for j in range(n_rows):
            current_cell = assignment[(j,i)]
            if current_cell == None:
                current_cell = 0
            filled_count += current_cell
            if current_cell == 0:
                filled_list.append(filled_count)
                filled_count = 0
            if j == n_rows - 1:
                filled_list.append(filled_count)
        # remove 0's from filled_list
        filled_list = [x for x in filled_list if x != 0]	
        check_cols.append(filled_list)  
    return check_rows, check_cols

def simple_spaces(csp, assignment):
    row_constraints = csp.row_constraints
    col_constraints = csp.col_constraints
    n_rows = csp.n_rows
    n_cols = csp.n_cols
    # check rows first
    check_rows = []
    check_cols = []
    for i in range(n_rows):
        # count 1's in row from left to right
        # if 0 is encountered, then start counting again
        filled_count = 0
        filled_list= []
        zero_encountered = False
        for j in range(n_cols):
            current_cell = assignment[(i,j)]
            if current_cell == None:
                current_cell = 0
            filled_list.append(current_cell)
        # remove 0's from filled_list
        #filled_list = [x for x in filled_list if x != 0]	
        check_rows.append(filled_list)
    for i in range(n_cols):
        # count 1's in row from left to right
        # if 0 is encountered, then start counting again
        filled_count = 0
        filled_list= []
        zero_encountered = False
        for j in range(n_rows):
            current_cell = assignment[(j,i)]
            if current_cell == None:
                current_cell = 0
            filled_list.append(current_cell)
        # remove 0's from filled_list
        #filled_list = [x for x in filled_list if x != 0]	
        check_cols.append(filled_list)  
    return check_rows, check_cols

# get list indices
def get_indices(lst, element):
    return [i for i, e in enumerate(lst) if e == element]

def get_contiguous_ranges(nums):
    if nums == []:
        return []
    ranges = []
    start = end = nums[0]
    for i in range(1, len(nums)):
        if nums[i] == end + 1:
            end = nums[i]
        else:
            ranges.append((start, end))
            start = end = nums[i]
    ranges.append((start, end))
    return [r for r in ranges if r[0] <= r[1]]

def pad_a_list(a_list, contiguous_ranges, padding):
    for (start, end), pad in zip(contiguous_ranges, padding):
        # Pad left
        for i in range(start - pad, start):
            if i >= 0:
                a_list[i] = 1

        # Pad right
        for i in range(end + 1, end + 1 + pad):
            if i < len(a_list):
                a_list[i] = 1

    return a_list


def sum_constraints_with_spaces(constraint_sums, constraint_groups):
    sum_cws = []
    for i in range(len(constraint_groups)):
        spaces_between = constraint_groups[i] - 1 
        sum_cws.append(constraint_sums[i] + spaces_between)
    return sum_cws

# see https://en.wikipedia.org/wiki/Nonogram "mathematical approach"
def step_two_math_approach(constraint_sums, constraint_groups, n_rows_or_cols):
    sum_clues = sum_constraints_with_spaces(constraint_sums, constraint_groups)
    return [n_rows_or_cols - sum_clues[i] for i in range(len(sum_clues))]

def confirmed_filled_in(constraints, constraint_sums, constraint_groups, n_rows_or_cols):
    help_n = step_two_math_approach(constraint_sums, constraint_groups, n_rows_or_cols)
    confirmed= [[] for _ in range(n_rows_or_cols)]
    for i in range(n_rows_or_cols):
        current_constraints = constraints[i]
        for j in range(len(current_constraints)):
            confirmed[i].append(current_constraints[j]-help_n[i])
    return confirmed

def fill_portion(assignment, index, start, end, value, is_row=True):
    for k in range(start, end):
        key = (index, k) if is_row else (k, index)
        assignment[key] = value

def fill_in_confirmed(constraints, confirmed_list, assignment, n_rows, n_cols, fill_in, row=True):
    n = n_rows if row else n_cols
    for i in range(n):
        current_constraints = constraints[i]
        current_confirmed = confirmed_list[i]
        start_index = 0
        end_index = 0
        for j, confirmed_n in enumerate(current_constraints):
            end_index += confirmed_n
            start_index += confirmed_n - current_confirmed[j]
            fill_portion(assignment, i, start_index, end_index, fill_in, is_row=row)
            start_index += (1 + end_index)
            end_index += 1


def confirmed_spaces(confirmed_rows, confirmed_cols, constraints, constraint_sums, constraint_groups, n_rows_or_cols):
    help_n = step_two_math_approach(constraint_sums, constraint_groups, n_rows_or_cols)
    confirmed= [[] for _ in range(n_rows_or_cols)]
    for i in range(n_rows_or_cols):
        current_constraints = constraints[i]
        for j in range(len(current_constraints)):
            confirmed[i].append(current_constraints[j]-help_n[i])
    return confirmed


def print_assignment(csp, assignment):
    n_rows = csp.n_rows
    n_cols = csp.n_cols
    # print assignment, # where 1, . where 0, x where None
    for i in range(n_rows):
        for j in range(n_cols):
            if assignment[(i,j)] == 1:
                print(" #", end="")
            elif assignment[(i,j)] == 0:
                print(" .", end="")
            else:
                print(" x", end="")
        print()