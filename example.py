import numpy as np
import cutting_plane

if __name__ == '__main__':
    # --------------------------- QUESTION 1 --------------------------- #

    # Maximize 3𝑥 + 2𝑦
    # Subject to:
    # 3𝑥+𝑦≤6
    # 𝑦≤2
    # 𝑥,𝑦≥0

    # Define the objective function coefficients
    c = np.array([3, 2])
    # Define the constraints' right-hand side values
    b = np.array([6, 2])
    # Define the constraints' coefficients
    A = np.array([
        [3, 1],
        [0, 1]
    ])

    # Call the solve function with debug output enabled
    cutting_plane.solve(c, b, A, True)

    # --------------------------- QUESTION 2 --------------------------- #

    # # Maximize 14𝑥1 + 16𝑥2
    # # Subject to:
    # # 4𝑥1 + 3𝑥2 <= 12
    # # 6𝑥1 + 8𝑥2 <= 24
    # # 𝑥1, 𝑥2 >= 0

    # # Define the objective function coefficients
    # c = np.array([14, 16])
    # # Define the constraints' right-hand side values
    # b = np.array([12, 24])
    # # Define the constraints' coefficients
    # A = np.array([
    #     [4, 3],
    #     [6, 8]
    # ])

    # # Call the solve function with debug output enabled
    # cutting_plane.solve(c, b, A, True)