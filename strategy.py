from model import Model

class Strategy():
    def __init__(self, search_order=0, max_depth=20):
        self.frontier = []
        self.explored = []
        self.zeros = []
        self.path = []
        self.model = Model()
        self.max_depth = max_depth
        self.current_depth = 0