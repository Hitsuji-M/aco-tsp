import numpy as np
import random

from dataclasses import dataclass

@dataclass()
class Path:
    path: list[tuple[int, int]]
    weight: int = np.inf

    def __lt__(self, other):
        if not isinstance(other, Path): raise TypeError(f"'<' not supported between instances of '{type(self)}' and '{type(other)}'")
        return self.weight < other.weight

    def __gt__(self, other):
        if not isinstance(other, Path): raise TypeError(f"'>' not supported between instances of '{type(self)}' and '{type(other)}'")
        return self.weight > other.weight

    def __le__(self, other):
        if not isinstance(other, Path): raise TypeError(f"'<=' not supported between instances of '{type(self)}' and '{type(other)}'")
        return self.weight <= other.weight

    def __ge__(self, other):
        if not isinstance(other, Path): raise TypeError(f"'>=' not supported between instances of '{type(self)}' and '{type(other)}'")
        return self.weight >= other.weight


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
        A boolean to determine if the ants should start at a random city or always at the city #0
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


    def get_path_weight(self, path: list[tuple[int, int]]) -> int:
        distance = 0

        for move in path:
            distance += self.cities[move]
        return distance


    def generate_path(self, start: int) -> Path:
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
        weight = self.get_path_weight(path)
        return Path(path, weight)


    def get_paths(self) -> list[Path]:
        paths: list[Path] = []
        for _ in range(self.n_ants):
            start = random.randint(0, self.n_cities) if self.random_start else 0
            paths.append(self.generate_path(start))
        return paths

    
    def add_pheromones(self, path: Path) -> None:
        raise NotImplementedError("The function to add pheromones on the path is not implemented")


    def generate_decay(self) -> None:
        raise NotImplementedError("the decay handling function is not implemented")
        

    def find_best(self, print_best: bool) -> Path:
        res: Path = None
        best_path: Path = None
        
        for _ in range(self.n_iter):
            paths = self.get_paths()
            best_path = min(paths)

            if best_path < res:
                res = best_path

            #self.generate_decay()
            #self.add_pheromones(None)
        return res