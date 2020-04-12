from strategy import Strategy
import numpy as np
from hashlib import sha256


class DFS(Strategy):

    def __init__(self, search_order="DLRU"):
        search_order = search_order[::-1]
        Strategy.__init__(self, search_order=search_order)

    def run(self):
        flag = self.model.is_solved()
        while not flag:
            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(
                self.model.current_state).hexdigest()] = True
            ops = self.model.get_operators()

            path = self.path.pop()

            if not len(path) > self.max_depth - 1:
                for op in ops:
                    new_state, new_zero = self.model.get_neighbour_state(op)
                    new_state_hash = sha256(new_state).hexdigest()
                    if not self.frontier_hash[new_state_hash] and not self.explored_hash[new_state_hash]:
                        # add current state to frontier
                        self.frontier.append(new_state)
                        self.frontier_hash[new_state_hash] = True
                        # add current zero position to zeros list(like frontier)
                        self.zeros.append(new_zero)
                        # add operation to path
                        new_path = list(path)
                        new_path.append(op)
                        self.path.append(new_path)
            if not len(self.frontier) and len(self.explored) and not len(self.path):
                print('Solution not found')
                return -1
            self.model.current_state = np.copy(self.frontier[-1])
            self.model.zero_position = self.zeros[-1]
            state_hash = sha256(self.model.current_state).hexdigest()
            self.frontier_hash[state_hash] = False
            del self.frontier[-1]
            del self.zeros[-1]
            flag = self.model.is_solved()


if __name__ == "__main__":
    dfs = DFS(search_order="RDLU")
    print(dfs.model)
    result = dfs.run()
    print(dfs.model)
    print(dfs.path[-1])
    # order = list("LRUD")
    # x = set()
    # for _ in range(30):
    #     shuffle(order)
    #     x.add(''.join(order))

    # for order in x:
    #     dfs = DFS(search_order=order)
    #     start_zero = dfs.model.zero_position
    #     print("start -> ", start_zero)
    #     dfs.start()
    #     end_zero = dfs.model.zero_position
    #     if end_zero == (3, 3) and start_zero != (3, 3):
    #         print(start_zero, end_zero)
    #         print(dfs.path[-1])
