import numpy as np
import random

class ACO:
    """
    Class for the Ant Colony Optimization algorithm.

    Attributes
    ----------
    cities : numpy.ndarray
        The cities matrix composing the TSP problem
    n_cities : int
        The number of cities composing the problem
    pheromones : numpy.ndarray
        The pheromones for each arcs
    n_ants : int
        Number of ants involved in the algorithm
    n_iter : int
        Number of iterations before stopping the algorithm
    decay : float
        The factor for pheromones' decay 
    """

    def __init__(
        self,
        cities: np.ndarray,
        n_cities: int,
        n_ants: int,
        n_iter: int,
        decay: float
    ) -> None:

        self.cities = cities
        self.n_cities = n_cities
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.decay = decay
        
        self.pheromones = np.ones(self.cities.shape) / 2


    def choose_city(self, start: int, visited: set) -> int:
        availables = set([range(self.n_cities)]) - visited
        values = [0.0 for _ in range(availables)]
        arcs = self.cities[start]
        complete_score = 0

        for idx in availables:
            complete_score += self.pheromones[start, idx] / arcs[idx]

        for idx in availables:
            values[idx] = (self.pheromones[start, idx] / arcs[idx]) / complete_score
        
        return random.choices(availables, weights=values)


    def find_best(self) -> tuple[list, int]:
        best_path = ([], np.inf)
        path = []
        
        for _ in range(self.n_iter):
            parkour = np.sum(path)
            if parkour < best_path[1]:
                best_path = (path, parkour)
        return best_path