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

        best_state = self.model.current_state
        best_zero = self.model.zero_position
        best_move = None

        while True:
            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(self.model.current_state).hexdigest()] = True

            best_f_value = 241

            ops = self.model.get_operators()

            for op in ops:
                new_state, new_zero = self.model.get_neighbour_state(op)
                new_state_hash = sha256(new_state).hexdigest()

                f_value = self.model.get_f_value(new_state, self.current_depth)

                if f_value == 0:
                    self.path[0].append(op)
                    return self.path[0]

                elif not self.explored_hash[new_state_hash] and f_value < best_f_value:
                    best_f_value = f_value
                    best_state = new_state
                    best_zero = new_zero
                    best_move = op
            self.path[0].append(best_move)
            self.model.current_state = np.copy(best_state)
            self.model.zero_position = best_zero
            self.current_depth += 1
