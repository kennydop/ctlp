import numpy as np

def make_tableau(c, b, A):
    n = len(c)
    m = len(b)

    simplex_tableau = np.hstack((A, np.identity(m), np.zeros((m, 1)), np.array([b]).T))
    simplex_tableau = np.vstack((simplex_tableau, np.array([np.hstack((-c, np.zeros(m), np.ones(1), np.zeros(1)))])))

    return simplex_tableau

def solve(c, b, A, debug_output=False, blands_rule=False):
    n = len(c)
    m = len(b)

    simplex_tableau = make_tableau(c, b, A)

    return solve_tableau(n, m, simplex_tableau, debug_output, blands_rule)

def solve_tableau(n, m, simplex_tableau, debug_output=False, blands_rule=False):
    if debug_output:
        print("Simplex tableau :")
        print(format_tableau(simplex_tableau))

    while True:
        # Column selection
        # Equivalent to searching for the variable in the base that would increase the output function the most
        optimal = True
        column = 0
        if blands_rule:
            for i, e in enumerate(simplex_tableau[-1]):
                if e < 0:
                    optimal = False
                    column = i
                    break
        else:
            for i, e in enumerate(simplex_tableau[-1]):
                if e < 0:
                    optimal = False
                    if e < simplex_tableau[-1, column]:
                        column = i
        
        if optimal:
            if debug_output:
                print(format_tableau(simplex_tableau))
            break

        # Row selection
        # Equivalent to searching for the variable outside the base that constraints the augmentation of the output function the most (smallest b_i / leaving variable coefficient)
        row = -1
        for i in range(m):
            # Only positive entries are considered
            if simplex_tableau[i, column] <= 0:
                continue
            if row == -1 or simplex_tableau[row, -1] / simplex_tableau[row, column] > simplex_tableau[i, -1] / simplex_tableau[i, column]:
                row = i
        if row == -1:
            raise Exception(f"Unbounded solutions in tableau (selected column : {column})", simplex_tableau)
    
        pivot = simplex_tableau[row, column]
        simplex_tableau[row] /= pivot
    
        for r in range(len(simplex_tableau)):
            if r != row:
                simplex_tableau[r] -= simplex_tableau[row] * simplex_tableau[r, column] 
    
        if debug_output:
            print("Current simplex tableau :")
            print(format_tableau(simplex_tableau))

    return simplex_tableau

# Returns an array of basic variables (row, column, value)
def get_basic_variables(simplex_tableau):
    x = []

    # We are excluding the last two columns as they do not contain variables
    for i in range(len(simplex_tableau.T) - 2):
        nonzeros = 0
        nonones = 0
        oneidx = -1
        for cidx, c in enumerate(simplex_tableau.T[i]):
            if c != 0:
                nonzeros += 1
            if c != 1:
                nonones += 1
            if c == 1:
                oneidx = cidx
    
        if nonzeros == 1 and nonones == len(simplex_tableau.T[i]) - 1:
            # This is a basic variable
            x.append((oneidx, i, simplex_tableau[oneidx, -1]))
    
    return x

def add_constraint(simplex_tableau, constraint_row, constraint_b_value):
    rows, columns = simplex_tableau.shape

    constraint_row = np.concatenate((constraint_row, [1.0, 0.0, constraint_b_value]))

    simplex_tableau = np.insert(simplex_tableau, -2, np.zeros(rows), axis=1)
    simplex_tableau = np.insert(simplex_tableau, -1, constraint_row, axis=0)

    slack_variable = np.zeros(rows)
    slack_variable[-2] = 1
    slack_variable = np.array([slack_variable])

    return simplex_tableau

def format_tableau(tableau):
    formatted_table = []
    num_rows, num_cols = tableau.shape

    # Typically, the number of decision variables will be the total columns minus slack variables, 'z', and 'b'
    # Slack variables count should match the number of constraints, which is the number of rows minus one for the objective function row
    num_slack_vars = num_rows - 1
    num_decision_vars = num_cols - num_slack_vars - 2  # Adjusted to include all decision variables

    # Determine the column widths by finding the maximum length of the float when converted to string, plus some padding
    col_widths = [max(len(f"{tableau[row, col]:.2f}") for row in range(num_rows)) + 3 for col in range(num_cols)]

    # Constructing headers
    headers = ["x_" + str(i+1) for i in range(num_decision_vars)] + \
              ["s_" + str(i+1) for i in range(num_slack_vars)] + ["z", "b"]
    
    # Format each row
    for row in tableau:
        formatted_row = " | ".join(f"{value:>{col_widths[col]}.2f}" for col, value in enumerate(row))
        formatted_table.append(formatted_row)

    # Add the headers
    formatted_table.insert(0, " | ".join(f"{headers[col]:>{col_widths[col]}}" for col in range(len(headers))))
    
    return "\n".join(formatted_table)






if __name__ == '__main__':
    print("Simplex algorithm")
    print("Maximize <c, x> subject to constraints Ax <= b, x_i >= 0, where A is an m*n matrix")
    print("==================")

    n = int(input("Size n (size of vector x) : "))
    m = int(input("Size m (amount of constraints) : "))

    print("c vector :")
    c = np.array([float(input("c_" + str(i) + " : ")) for i in range(n)])
    print("b vector :")
    b = np.array([float(input("b_" + str(i) + " : ")) for i in range(m)])
    print("A matrix :")
    A = []
    for i in range(m):
        A.append([float(input("A_" + str(i) + "," + str(j) + " : ")) for j in range(n)])
    A = np.array(A)

    solve(c, b, A, True)