from strategy import Strategy
import numpy as np
from random import shuffle


class DFS(Strategy):

    def __init__(self, search_order="DLRU"):
        Strategy.__init__(self, search_order=search_order)

    def run(self):
        flag = -1
        while flag == -1:
            flag = self.start()

    def start(self, nodes_in_level=0, current_node=0):  # method running recursively
        if not self.model.is_solved(): # compare current state to solution
            if self.current_depth > self.max_depth:
                self.frontier = []
                self.zeros = []
                self.current_depth = 0
                self.path = [[]]
                return -1

            # add current state to explored
            self.explored.append(np.copy(self.model.current_state))
            ops = self.model.get_operators()  # get available operators

            # if current_node == nodes_in_level:  # if last node in level
                # self.current_depth += 1  # increase the depth level by one
                # nodes_in_level = len(ops)  # check available nodes in level
                # current_node = 0  # reset current node

            # pop the first item from the path list and expand on it
            path = self.path.pop()

            for op in ops:  # iterate over all available operators
                # get new state and zero position
                new_state, new_zero = self.model.get_neighbour_state(op)

                # represent if any of the arrays in frontier match with the new array
                flagFrontier = False
                for row in self.frontier:
                    if np.array_equal(new_state, row):
                        flagFrontier = True
                        break

                # represent if any of the arrays in explored match with the new array
                flagExplored = False
                for row in self.explored:
                    if np.array_equal(new_state, row):
                        flagExplored = True
                        break

                if not flagFrontier and not flagExplored:
                    # add current state to frontier
                    self.frontier.append(new_state)
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
            # del self.frontier[-1]
            self.frontier.pop()

            # del zero position
            # del self.zeros[-1]
            self.zeros.pop()

            # if(self.current_depth == self.max_depth and self.current_width <= self.max_width):
            #     self.current_depth = 0
            #     self.model.current_state = np.copy(self.model.first_state)
            #     self.model.zero_position = tuple(self.model.first_zeros)
            #     self.current_width += 1
            #     self.start(0, 0)
            # else:
            #     return True
            self.current_depth += 1
            return self.start()
        else:
            return True

if __name__ == "__main__":
    dfs = DFS()
    print(dfs.model)
    dfs.run()
    print(dfs.model)
    print(dfs.path)
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