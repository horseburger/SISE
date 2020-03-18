from strategy import Strategy
import numpy as np
from hashlib import sha256


class DFS(Strategy):

    def __init__(self, search_order="DLRU"):
        search_order = search_order[::-1]
        Strategy.__init__(self, search_order=search_order)

    def run(self):
        flag = -1
        while flag == -1:
            flag = self.start()
        return flag

    def start(self):  # method running recursively
        if not self.model.is_solved(): # compare current state to solution
            if len(self.path[-1]) > self.max_depth:
                self.model.current_state = self.frontier.pop()
                self.model.zero_position = self.zeros.pop()
                self.path.pop()
                return -1
            elif not len(self.frontier) and len(self.explored):
                return -2

            # add current state to explored

            self.explored.append(np.copy(self.model.current_state))
            self.explored_hash[sha256(self.model.current_state).hexdigest()] = True
            ops = self.model.get_operators()  # get available operators


            # pop the first item from the path list and expand on it
            path = self.path.pop()

            for op in ops:  # iterate over all available operators
                # get new state and zero position
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

            # get last state from frontier
            self.model.current_state = np.copy(self.frontier[-1])

            # get last zero position from frontier
            self.model.zero_position = tuple(self.zeros[-1])

            # del state
            self.frontier.pop()

            # del zero position
            self.zeros.pop()

            self.current_depth += 1
            return self.start()
        else:
            return True

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
