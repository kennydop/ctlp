import simplex
import numpy as np
import math

EPSILON = 0.0001

def solve(c, b, A, debug_output=False, blands_rule=False):
    n = len(c)
    m = len(b)

    simplex_tableau = simplex.make_tableau(c, b, A)

    return solve_tableau(n, m, simplex_tableau, debug_output, blands_rule)

def solve_tableau(n, m, simplex_tableau, debug_output=False, blands_rule=False):
    while True:    
        if debug_output:
            print("Current simplex + cutting planes tableau :")
            print(simplex.format_tableau(simplex_tableau))

        # Solving the relaxed linear program
        solved_simplex_tableau = simplex.solve_tableau(n, m, simplex_tableau.copy(), False, blands_rule)

        if debug_output:
            print("Solved simplex + cutting planes tableau :")
            print(simplex.format_tableau(solved_simplex_tableau))

        # Finding a non integer basic variable
        basic_variables = simplex.get_basic_variables(solved_simplex_tableau)
        basic_variable_row = -1
        basic_variable_column = -1
        for row, column, value in basic_variables:
            # This is how we test if a value is close to an integer (we have to because of floating point precision errors)
            if not -EPSILON < value - round(value) < EPSILON:
                basic_variable_row = row
                basic_variable_column = column
                break
        else:
            # We found a solution
            if debug_output:
                print("Optimal cutting planes + simplex tableau found")
            simplex_tableau = solved_simplex_tableau
            break

        # Creating a linear constraint (used inequality : x_i + sum_j(floor(a_i,j)x_j) <= floor(b_i))
        constraint_row = np.zeros(n + m)
        for c in range(n + m):
            if c != basic_variable_column:
                constraint_row[c] = math.floor(solved_simplex_tableau[basic_variable_row, c])
        constraint_row[basic_variable_column] = 1.0
        constraint_b_value = math.floor(solved_simplex_tableau[basic_variable_row, -1])

        simplex_tableau = simplex.add_constraint(simplex_tableau, constraint_row, constraint_b_value)
        m += 1
    
    return simplex_tableau

    
if __name__ == '__main__':
    print("Cutting planes + simplex algorithm")
    print("Maximize <c, x> subject to constraints Ax <= b, x_i >= 0, x_i integer, where A is an m*n matrix")
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

    simplex_tableau = solve(c, b, A, True)

    exit(0)