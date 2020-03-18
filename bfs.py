from strategy import Strategy
import numpy as np
from hashlib import sha256

class BFS(Strategy):

    def __init__(self, search_order="LRUD"):
        Strategy.__init__(self, search_order=search_order)

    def run(self):
        flag = -1
        while flag == -1:
            flag = self.start()
        return flag

    def start(self):
        if not self.model.is_solved(): 
            #  and self.current_depth <= self.max_depth:
            if len(self.path[0]) > self.max_depth:
                self.model.current_state = self.model.first_state
                self.model.zero_position = self.model.first_zero
                self.path.pop(0)
                return -1

            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(self.model.current_state).hexdigest()] = True
            ops = self.model.get_operators()


            # pop the first item from the path list and expand on it
            path = self.path.pop(0)

            for op in ops:
                new_state, new_zero = self.model.get_neighbour_state(op)
                new_state_hash = sha256(new_state).hexdigest()

                if not self.frontier_hash[new_state_hash] and not self.explored_hash[new_state_hash]:
                    self.frontier.append(new_state)
                    self.frontier_hash[new_state_hash] = True
                    self.zeros.append(new_zero)
                    new_path = list(path)
                    new_path.append(op)
                    self.path.append(new_path)

            self.model.current_state = np.copy(self.frontier[0])
            self.model.zero_position = tuple(self.zeros[0])
            del self.frontier[0]
            del self.zeros[0]

            return self.start()
        else:
            return True


if __name__ == "__main__":
    bfs = BFS("RDLU")
    print(bfs.model)
    bfs.run()
    print(bfs.model)
    print(bfs.path[0])
