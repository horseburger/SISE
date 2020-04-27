from strategy import Strategy
import numpy as np
from hashlib import sha256


class ASTR(Strategy):
    def __init__(self, search_strategy="hamm"):
        Strategy.__init__(self, search_order="LRUD", max_depth=20,
                          heuristic=None, search_strategy=search_strategy)

    def run(self):
        if self.model.is_solved(self.model.current_state):
            return []
        path = []
        openStates = []
        closedStates = {}
        best_move = None

        while True:
            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(self.model.current_state).hexdigest()] = True

            best_f_value = 241

            ops = self.model.get_operators()

            for op in ops:
                new_state, new_zero = self.model.get_neighbour_state(op)
                new_state_hash = sha256(new_state).hexdigest()

                f_value = self.model.get_f_value(new_state)

                if f_value == 0:
                    return path + [op]

                f_value += self.current_depth
                if not self.explored_hash[new_state_hash] and not self.frontier_hash[new_state_hash] and f_value < best_f_value:
                    self.frontier_hash[new_state_hash] = True
                    openStates.append([f_value, new_state_hash, new_state, new_zero, path + [op]])

            sorted(openStates, key=lambda x: x[0])
            self.frontier_hash[openStates[0][1]] = False
            self.model.current_state = np.copy(openStates[0][2])
            self.model.zero_position = openStates[0][3]
            path = openStates[0][4]
            del openStates[0]
            self.current_depth += 1
