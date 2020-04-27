from strategy import Strategy
import numpy as np
from hashlib import sha256
from queue import PriorityQueue
from time import time


class ASTR(Strategy):
    def __init__(self, search_strategy="hamm"):
        Strategy.__init__(self, search_order="LRUD", max_depth=20,
                          heuristic=None, search_strategy=search_strategy)

    def run(self):
        start = time()
        if self.model.is_solved(self.model.current_state):
            return []
        path = []
        openStates = PriorityQueue()
        best_move = None

        while openStates:
            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(self.model.current_state).hexdigest()] = True

            ops = self.model.get_operators()

            max_f = 241
            for op in ops:
                new_state, new_zero = self.model.get_neighbour_state(op)
                new_state_hash = sha256(new_state).hexdigest()

                if self.model.is_solved(new_state):
                    return path + [op]

                f_value = self.model.get_f_value(new_state) + self.current_depth

                if not self.explored_hash[new_state_hash] and not self.frontier_hash[new_state_hash] and f_value <= max_f:
                    max_f = f_value
                    self.frontier_hash[new_state_hash] = True
                    openStates.put((f_value, [new_state_hash, new_state, new_zero, path + [op], self.current_depth]))

            key = openStates.get()[1]
            self.frontier_hash[key[0]] = False
            self.model.current_state = key[1]
            self.model.zero_position = key[2]
            path = key[3]
            self.current_depth = key[4]
            self.current_depth += 1
