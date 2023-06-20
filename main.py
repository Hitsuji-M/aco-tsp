import numpy as np

from aco import ACO

def read_from_file(filename) -> tuple[int, np.ndarray]:
    """
    Read the file and exports its data to create a matrix
    for the TSP problem.

    Originally created by Marco Baioletti
    """
    ncities = 0
    k = 0
    in_matrix = False
    m = []

    with open(filename, "r") as f:
        lines=f.readlines()

    for l in lines:
        if l.startswith("TYPE:"):
            if l.strip()[6:] != "TSP":
                raise TypeError("The file's type must 'TSP'")
        elif l.startswith("EDGE_WEIGHT_TYPE"):
            if l.strip()[18:] != "EXPLICIT":
                raise TypeError("The edges' weights must be of the type 'EXPLICIT'")
        elif l.startswith("EDGE_WEIGHT_FORMAT"):
            if l.strip()[20:] != "LOWER_DIAG_ROW":
                raise TypeError("The edges' format must be 'LOWER_DIAG_ROW")

        elif l.startswith("DIMENSION:"):
            ncities=int(l[11:].strip())
        elif l.startswith("EDGE_WEIGHT_SECTION"):
            in_matrix=True
        elif l.startswith("DISPLAY_DATA_SECTION") or l.startswith("EOF"):
            in_matrix=False
        elif in_matrix:
            m += [int(x) for x in l.strip().split(" ") if x != ""]

    matrix = np.zeros((ncities, ncities))
    for i in range(0,ncities):
        for j in range(0,i+1):
            distance = m[k]
            matrix[i,j] = distance if distance > 0 else np.inf
            k+=1

    for i in range(0, ncities):
        for j in range(i+1, ncities):
            matrix[i,j] = matrix[j,i]
    return ncities, matrix


def main():
    ncities, matrix = read_from_file("instances/gr120.tsp")
    n_ants = 1
    n_iter = 100
    decay = 0.5
    alpha = 1
    beta = 1

    aco = ACO(matrix, ncities, n_ants, n_iter, decay, alpha, beta)
    result = aco.find_best(False)

    print("\n ------- Solution ------- \n")
    print(result.path)
    print("==>", result.weight)


if __name__ == "__main__":
    main()