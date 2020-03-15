from strategy import Strategy
import numpy as np


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
            if len(self.path[0]) >= self.max_depth:
                self.model.current_state = self.model.first_state
                self.model.zero_position = self.model.first_zero
                self.path.pop(0)
                return -1

            self.explored.append(np.copy(self.model.current_state))
            ops = self.model.get_operators()

            # increase the depth level by one
            # if current_node == nodes_in_level:
            #     self.current_depth += 1
            #     nodes_in_level = len(ops)
            #     current_node = 0

            # pop the first item from the path list and expand on it
            path = self.path.pop(0)

            for op in ops:
                new_state, new_zero = self.model.get_neighbour_state(op)

                # check if any of the arrays in frontier or explored match with the new array
                flagFrontier = False
                for row in self.frontier:
                    if np.array_equal(new_state, row):
                        flagFrontier = True
                        break

                flagExplored = False
                for row in self.explored:
                    if np.array_equal(new_state, row):
                        flagExplored = True
                        break

                if not flagFrontier and not flagExplored:
                    self.frontier.append(new_state)
                    self.zeros.append(new_zero)
                    new_path = list(path)
                    new_path.append(op)
                    self.path.append(new_path)

            self.model.current_state = np.copy(self.frontier[0])
            self.model.zero_position = tuple(self.zeros[0])
            del self.frontier[0]
            del self.zeros[0]

            return self.run()
        else:
            return True


if __name__ == "__main__":
    bfs = BFS("RDLU")
    print(bfs.model)
    bfs.run()
    print(bfs.model)
    print(bfs.path[0])
