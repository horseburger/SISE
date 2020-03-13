from model import Model

class Strategy():
    def __init__(self):
        self.frontier = []
        self.explored = []
        self.model = Model()