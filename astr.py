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
        best_state = {}
        best_zero = {}
        best_move = {}
        while True:
            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(
                self.model.current_state).hexdigest()] = True
            best_f_value = self.model.get_f_value(
                self.model.current_state, self.current_depth)
            ops = self.model.get_operators()
            for op in ops:
                new_state, new_zero = self.model.get_neighbour_state(op)

                if self.model.is_solved(new_state):
                    return path + [op]

                f_value = self.model.get_f_value(new_state, self.current_depth)
                new_state_hash = sha256(new_state).hexdigest()
                if f_value == 0:
                    self.path[0].append(op)
                    return 0
                elif f_value < best_f_value and not self.explored_hash[new_state_hash]:
                    best_state[f_value] = new_state
                    best_zero[f_value] = new_zero
                    best_move[f_value] = op
            key = list(best_state.keys())[0]
            self.path[0].append(best_move[key])
            self.model.current_state = np.copy(best_state[key])
            self.model.zero_position = best_zero[key]
            best_state.clear()
            best_move.clear()
            best_zero.clear()
            self.current_depth += 1
