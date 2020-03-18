from bfs import BFS
from dfs import DFS
import numpy as np
import argparse
from random import shuffle
import sys
import time

sys.setrecursionlimit(10**5)
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

args = parser.parse_args()

def load_config(filename):
    with open(filename, 'r') as f:
        dimensions = [int(num) for num in f.readline().strip('\n').split(' ')]
        layout = []
        for row in range(dimensions[0]):
            layout += f.readline().strip('\n').split(' ')
    return dimensions, [int(num) for num in layout if num]


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

def randomize_search_order():
    order = list("LRUD")
    x = set()
    for _ in range(32):
        shuffle(order)
        x.add(''.join(order))

    return x
    


if __name__ == "__main__":

    orders = ["RDUL", "RDLU", "DRUL", "DRLU", "LUDR", "LURD", "ULDR", "ULRD"]

    dimensions, layout = load_config(args.start)
    start = time.time()
    if args.strategy == 'bfs':
        bfs = BFS(search_order=args.parameter)
        bfs.model.load_layout(dimensions, layout)
        bfs.run()
        end = time.time() - start
        print(bfs.model.zero_position, bfs.path[0])
    elif args.strategy == 'dfs':
        dfs = DFS(search_order=args.parameter)
        dfs.model.load_layout(dimensions, layout)
        dfs.run()
        end = time.time() - start
        print(dfs.path[-1], dfs.model.zero_position)
    start = time.time()
    # for i in randomize_search_order():
    #     bfs = BFS(search_order=i)
    #     dims, lay = load_config("puzzles/4x4_07_00002.txt")
    #     bfs.model.load_layout(dims, lay)
    #     flag = bfs.run()
    #     # print(bfs.model.first_state)
    #     print(i, bfs.path[-1], flag)

    print(time.time() - start)
