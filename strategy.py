from model import Model

class Strategy():
    def __init__(self, search_order="LRUD", max_depth=20, heuristic=None):
        self.frontier = []
        self.explored = []
        self.zeros = []
        self.path = []
        self.model = Model(search_order=search_order, heuristic=heuristic)
        self.max_depth = max_depth
        self.current_depth = 0