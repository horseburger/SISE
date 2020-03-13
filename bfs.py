from strategy import Strategy
import numpy as np

class BFS(Strategy):

    def start(self):
        if not self.model.is_solved():
            print(bfs.model.current_state)
            self.run(0, 0)

    def run(self, nodes_in_level, current_node):
        operators = []
        if not self.model.is_solved() and self.current_depth <= self.max_depth:
            self.explored.append(np.copy(self.model.current_state))
            ops = self.model.get_operators()

            if current_node == nodes_in_level:
                self.current_depth += 1
                nodes_in_level = len(ops)
                current_node = 0

                
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

                if not flagFrontier or not flagExplored:
                    self.frontier.append(new_state)
                    self.zeros.append(new_zero)
                    operators.append(op)

            
            self.model.current_state = np.copy(self.frontier[0])
            self.model.zero_position = tuple(self.zeros[0])
            del self.frontier[0]
            del self.zeros[0]
            self.run(nodes_in_level, current_node + 1)

        else:
            print(self.current_depth)
            print(self.model.is_solved())
            return


if __name__ == "__main__":
    bfs = BFS()
    bfs.start()