import numpy as np
import random

from dataclasses import dataclass

@dataclass()
class Path:
    """
    Dataclass representing a path completing the TSP problem.

    Attributes
    ----------
    path : list[tuple[int, int]]
        The path took by the ant to complete the problem
    weight : int
        The complete weight of the path
    """
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
        
        self.pheromones = np.ones(self.cities.shape)
        self.random_start = False

    
    def set_random_start(self, random_start: bool) -> None:
        """Set random start attribute"""
        self.random_start = random_start


    def choose_city(self, start: int, visited: set) -> int:
        """
        Choose the next city to move in
        Probability of choosing a city is equal to
        `(pheromones^(alpha) * (1/distance)^(beta)) / (Sum of all the availables path's score)`

        Args:
        -----
        start : int
            The index of city corresponding to the ant current position
        visited : set
            A set of all the indexes of the already visited cities

        Returns:
        --------
        int
            The index of the chosen city        
        """
        availables = set(range(self.n_cities)) - visited
        values = [0.0 for _ in range(len(availables))]
        arcs = self.cities[start]
        complete_score = 0

        # Score computing corresponding to the formula (docstring)
        score = lambda y, x: (self.pheromones[x,y]**self.alpha) * (1/arcs[y])**self.beta

        for num in availables:
            complete_score += score(num, start)

        for idx, num in enumerate(availables):
            values[idx] = score(num, start) / complete_score # Probability calculation

        return random.choices(list(availables), weights=values)[0]


    def get_path_weight(self, path: list[tuple[int, int]]) -> int:
        """Compute the total distance of the path"""
        distance = 0

        for move in path:
            distance += self.cities[move]
        return distance


    def generate_path(self, start: int) -> Path:
        """
        Generate a path from the given starting point
        this path goes by each city once and finish at the starting one.
        """
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
        """Get the paths of each ant in this iteration"""
        paths: list[Path] = []
        for _ in range(self.n_ants):
            start = random.randint(0, self.n_cities) if self.random_start else 0
            paths.append(self.generate_path(start))
        return paths

    
    def add_pheromones(self, path: Path) -> None:
        """
        Add pheromones of the best path only
        Calculted in this way, `pheromones = pheromones + (1 / distance) 
        """
        for move in path.path:
            self.pheromones[move] += 1 / self.cities[move]
            self.pheromones[move[::-1]] += 1 / self.cities[move[::-1]] # We have a symetric TSP


    def evaporation(self) -> None:
        """Execute the evaportation of the pheromones with decay factor"""
        self.pheromones *= self.decay
        

    def find_best(self, print_best: bool) -> Path:
        """
        Find the best path out of all the iterations

        Args:
        -----
        print_best : bool
            Boolean to decide if you want the best path of each iteration

        Returns:
        --------
        Path
            The best path found among all the iterations
        """
        res: Path = Path(None)
        best_path: Path = None
        
        for _ in range(self.n_iter):
            paths = self.get_paths()
            best_path = min(paths)

            if best_path < res:
                res = best_path

            self.add_pheromones(best_path)
            self.evaporation()
            if print_best: print(best_path)
        return res