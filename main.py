import numpy as np
import time
import sys

from aco import ACO
from os import listdir

def read_from_file(filename) -> tuple[int, np.ndarray]:
    """
    Read the file and exports its data to create a matrix
    for the TSP problem.

    Originally created by Marco Baioletti

    Args:
    -----
    filename : str
        Name of the file containing cities data for TSP

    Raises:
    -------
    TypeError
        The file's data is not in the good format or type

    Returns:
    --------
    tuple[int, np.ndarray]
        Tuple containing the number of cities and the matrix with the distances
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
    """Main function lauched by default. Execute the ACO on all the files in `instances` repository"""
    n_ants = 5
    n_iter = 100
    decay = 0.75
    alpha = 1
    beta = 1
    random_start = False

    lines = [
        " ##### Results ##### ",
        "",
        "Params :",
        "--------",
        f"• Number of ants : {n_ants}",
        f"• Number of iterations : {n_iter}",
        f"• Decay factor : {decay}",
        f"• Pheromones and distance weights : {alpha} / {beta}",
        f"• Random start : {random_start}"
    ]

    with open("res.txt", "w") as res:
        res.write("\n".join(lines) + "\n")
 
        files = listdir("instances/")
        for file in files:
            if not file.endswith(".tsp"):
                continue

            ncities, matrix = read_from_file(f"instances/{file}")
            aco = ACO(matrix, ncities, n_ants, n_iter, decay, alpha, beta)
            aco.set_random_start(random_start)

            before = time.time()
            result = aco.find_best(False)
            after = time.time()
            delta = round(after - before, 5)

            res.write("\n\n")
            res.write(f"--- {file} ---\n")
            res.write(f"• Number of cities : {ncities}\n")
            res.write(f"• Weight result : {result.weight}\n")
            res.write(f"• Time spent : {delta}\n")
            res.write(str(result.path))

            print(f"{file} ({ncities} cities) ==> {delta}\n")

def single_exec(filename: str):
    """
    The function to execute the ACO on only one file

    Args:
    -----
    filename : str
        The name of the file that will create the distances matrix
    """
    n_ants = 10
    n_iter = 100
    decay = 0.75
    alpha = 1
    beta = 1
    random_start = False

    ncities, matrix = read_from_file(f"instances/{filename}")
    aco = ACO(matrix, ncities, n_ants, n_iter, decay, alpha, beta)
    aco.set_random_start(random_start)
    
    result = aco.find_best(True)
    print("\n\nWeight :", result.weight)
    print(result.path)

if __name__ == "__main__":
    if len(sys.argv) == 3 and (sys.argv[1] == "single" or sys.argv[1] == "-s"):
        single_exec(sys.argv[2])
    else:
        main()