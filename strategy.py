from model import Model
from collections import defaultdict
from sys import setrecursionlimit


class Strategy():
    setrecursionlimit(10**5)

    def __init__(self, search_order="LRUD", max_depth=20, heuristic=None):
        self.frontier = []
        self.explored = []
        self.frontier_hash = defaultdict(bool)
        self.explored_hash = defaultdict(bool)
        self.zeros = []
        self.path = [[]]
        self.model = Model(search_order=search_order, heuristic=heuristic)
        self.max_depth = max_depth
        self.current_depth = 0
        self.deepest = 0

    def get_recursion_depth(self):
        return max([len(steps) for steps in path])
