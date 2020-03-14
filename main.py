from bfs import BFS
from dfs import DFS
import numpy as np
import argparse


# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="Choose between bfs, dfs and astr", choices=[
                    "bfs", "dfs", "astr"])
parser.add_argument(
    "parameter", help="Choose the search order (LRUD) or the heurictic (hamm, manh)")
parser.add_argument(
    "start", help="File name with the starting order of the puzzle")
parser.add_argument("output", help="Result filename")
parser.add_argument("info", help="Additional info filename")

# args = parser.parse_args()


def load_config(filename):
    with open(filename, 'r') as f:
        dimensions = f.readline().strip('\n').split(' ')
        layout = f.readline().strip('\n').split(' ')
    return [int(num) for num in dimensions if num], [int(num) for num in layout if num]


def save_result(filename, result):
    with open(filename, 'w+') as f:
        f.write(str(len(result)) + '\n')
        f.write(','.join(result))


def save_info(filename, result_length, frontier_length, explored_length, max_depth, time):
    with open(filename, 'w+') as f:
        f.write(str(result_length) + '\n')
        f.write(str(explored_length) + '\n')
        f.write(str(frontier_length) + '\n')
        f.write(str(max_depth) + '\n')
        f.write(str(time) + '\n')


if __name__ == "__main__":
    bfs = BFS()
    dfs = DFS()
    dfs.model.current_state = np.copy(bfs.model.current_state)
    dfs.model.first_state = np.copy(bfs.model.current_state)
    dfs.model.first_zeros = tuple(bfs.model.zero_position)
    dfs.model.zero_position = tuple(bfs.model.zero_position)
    if bfs.start():
        save_result('BFS', bfs.path[0])
        print(bfs.model, bfs.path[0])
    if dfs.start():
        save_result('DFS', dfs.path[0])
        print(dfs.model, dfs.path[0])
