from bfs import BFS
from dfs import DFS
import numpy as np
import argparse
from random import shuffle
import time

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


def load_config(filename):
    with open(filename, 'r') as f:
        dimensions = [int(num) for num in f.readline().strip('\n').split(' ')]
        layout = []
        for row in range(dimensions[0]):
            layout += f.readline().strip('\n').split(' ')
    return dimensions, [int(num) for num in layout if num]


def save_result(filename, result, l):
    with open(filename, 'w+') as f:
        f.write(str(l) + '\n')
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
    args = parser.parse_args()

    dimensions, layout = load_config(args.start)
    if args.strategy == 'bfs':
        bfs = BFS(search_order=args.parameter)
        bfs.model.load_layout(dimensions, layout)
        start = time.time()
        bfs.run()
        end = round((time.time() - start) * 1000, 3)
        save_result(args.output, bfs.path[0], len(bfs.path[0]))
        save_info(args.info, len(bfs.path[0]), len(bfs.frontier) + len(bfs.explored), len(bfs.explored), len(bfs.path[0]), end)
    elif args.strategy == 'dfs':
        dfs = DFS(search_order=args.parameter)
        dfs.model.load_layout(dimensions, layout)
        start = time.time()
        r = dfs.run()
        end = round((time.time() - start) * 1000, 3)
        if not r:
            save_result(args.output, dfs.path[-1], len(dfs.path[-1]))
            save_info(args.info, len(dfs.path[-1]), len(dfs.frontier) + len(dfs.explored), len(dfs.explored), dfs.deepest, end)
        else:
            save_result(args.output, [], -1)
            save_info(args.info, -1, len(dfs.frontier) + len(dfs.explored), len(dfs.explored), dfs.deepest, end)
