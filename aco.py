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
    alpha : int
        Weight of the pheromones when computing city probability
    beta : int
        Weight of the distance when computing city probability
    random_start : bool
    """

    def __init__(
        self,
        cities: np.ndarray,
        n_cities: int,
        n_ants: int,
        n_iter: int,
        decay: float,
        alpha: int,
        beta: int
    ) -> None:

        self.cities = cities
        self.n_cities = n_cities
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        
        self.pheromones = np.ones(self.cities.shape) / 2
        self.random_start = False

    
    def set_random_start(self, random_start: bool) -> None:
        self.random_start = random_start


    def choose_city(self, start: int, visited: set) -> int:
        availables = set(range(self.n_cities)) - visited
        values = [0.0 for _ in range(len(availables))]
        arcs = self.cities[start]
        complete_score = 0

        score = lambda y, x: (self.pheromones[x,y]**self.alpha) * (1/arcs[y])**self.beta

        for num in availables:
            complete_score += score(num, start)

        for idx, num in enumerate(availables):
            values[idx] = score(num, start) / complete_score

        return random.choices(list(availables), weights=values)[0]


    def generate_path(self, start: int) -> list[tuple[int, int]]:
        previous = start
        path = []
        visited = set()

        visited.add(start)
        for _ in range(self.n_cities - 1):
            city = self.choose_city(previous, visited)
            path.append((previous, city))
            visited.add(city)
            previous = city

        path.append((previous, start))
        return path

    
    def get_path_weight(self, path: list[tuple[int, int]]) -> int:
        distance = 0

        for move in path:
            distance += self.cities[move]
        return distance


    def get_paths(self) -> list[list[tuple[int, int]]]:
        paths: list[list[tuple[int, int]]] = []
        for _ in range(self.n_ants):
            start = random.randint(0, self.n_cities) if self.random_start else 0
            paths.append(self.generate_path(start))
        return paths

    
    def add_pheromones(self, path: list[tuple[int, int]]) -> None:
        raise NotImplementedError("The function to add pheromones on the path is not implemented")


    def generate_decay(self) -> None:
        raise NotImplementedError("the decay handling function is not implemented")
        

    def find_best(self, print_best: bool) -> tuple[list, int]:
        best_path = ([], np.inf)
        path = []
        
        for _ in range(self.n_iter):
            self.get_paths()
            #self.generate_decay()
            #self.add_pheromones(None)
        return best_path