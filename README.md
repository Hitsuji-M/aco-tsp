This is an implementation of the Ant Colony Optimization (ACO) algortithm for the Travelling Salesman Problem (TSP) with symetric arcs. Created for my project in the course **Computational Intelligence**.

## Launch the project

- Clone and move into the repository
- Execute the main file `python3 main.py` 
  - This will execute all the files in the `instances folder`
  - You can add 2 parameters `-s` / `single` and the name of the file to perform the algorithm on one file : `python3 main.py -s gr17.tsp`

- With the default execution you will find all the results in a `res.txt` file.

## ACO explanation

This implementation works with symetric graph. The arc length are generated from the instances files where all the cities are linked one to another. For the arc city linking city n to n, its weight is equal to `numpy.inf`.

When executing the ACO we need to provide several arguments :
- `cities` : A 2D array containing for each city its arc weight to the others cities.
- `n_cities` : The number of cities of the current TSP problem
- `n_ants` : The number of ants that will create a path per iteration
- `n_iter` : The number of iterations to execute before returning the best path found
- `decay` : A float number between ]0;1] representing the evaporation of the pheromones at each iteration. Greater is the decay factor the less the pheromones will evaporate.
- `alpha` : The pheromones weight factor
- `beta` : The distances weight factor

### How the solution is found :
- At each iteration we generate a path from each ant. The more ants there are the more chances there will be to obtain a great path.
  - To create a path an ant will start at a city (it can be set to random, otherwise they all start at city n°0) and for each available city (it excludes already visited cities) from where they are, the will compute the probability to go to the next city. Then they randomly choose a city using these probabilities as weights. Note that more ants means also multiplying the paths generations and the time to obtain a result.
  - The probability is calculated this way : `score(city) / sum_score_available_cities` where `score = pheromones_value^(alpha) * (1/distance)^(beta)`. The distance is the value of the arc, which corresponds to the heuristic value of the ACO. That means that the pheromones quantity will affect the probability of being chosen.

- Once all the paths have been generated, we choose the best one, which corresponds to the shortest.
- We can now add pheromones on the best path found in this iteration corresponding to : `pheromone[i][j] = pheromone[i][j] + 1/heuristic_value` where i is the starting city of the move, j the arrival and the heuristic value is the distance between the cities (arc value). We do that for each move in the path.
- Then we can execute the evaporation of the pheromones, having a low evaporation will increase the possibility of having a path quickly chosen because it will be prefered. A high evaporation, will increase the possibility of changing the path at each interaction.
- Once we done this, we compare the solution found to the current best, and choose the one with the smaller path length.
- After all the iterations we can return the best path found !
