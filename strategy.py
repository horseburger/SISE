from model import Model
from collections import defaultdict


class Strategy():
    def __init__(self, search_order="LRUD", max_depth=7, max_width=20, heuristic=None):
        self.frontier = []
        self.explored = []
        self.frontier_hash = defaultdict(bool)
        self.explored_hash = defaultdict(bool)
        self.zeros = []
        self.path = [[]]
        self.model = Model(search_order=search_order, heuristic=heuristic)
        self.max_depth = max_depth
        self.max_width = max_width
        self.current_depth = 0
        self.current_width = 0
        self.current_depth = 0

    def get_recursion_depth(self):
        return max([len(steps) for steps in path])
