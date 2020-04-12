import matplotlib.pyplot as plt
from bfs import BFS
from dfs import DFS
from main import load_config, save_info, save_result

from os import listdir, makedirs, path
from collections import defaultdict
from time import time
from statistics import mean
import numpy as np
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


orders = ["RDUL", "RDLU", "DRUL", "DRLU", "LUDR", "LURD", "ULDR", "ULRD"]
puzzles = listdir("./puzzles")
criterions = ["path_length", "frontier", "explored", "depth", "time"]

# {alg: order: depth: criterions}
results = {key:defaultdict(dict) for key in "BFS DFS A*".split(' ')}
for foo in results:
    results[foo] = {key:defaultdict(list) for key in orders}


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def process_results(algo): 
    # {criterion: depth: []}
    avg_whole = {key: defaultdict(list) for key in criterions}
    for crit in criterions:
        for l in range(1, 8):
            foo = []
            for order in orders:
                foo += [results[algo][order][l][i][crit] for i in range(len(results[algo][order][l]))]
            avg_whole[crit][l] = foo
    # {criterion: depth: order: }
    avg_orders = {key: defaultdict(dict) for key in criterions}
    for foo in avg_orders:
        # bfs_avg_orders[foo] = {key: defaultdict for key in range(1, 8)}
        for key in range(1, 8):
            avg_orders[foo][key] = {order: list() for order in orders}

    for crit in criterions:
        for depth in avg_orders[crit]:
            for order in orders:
                avg_orders[crit][depth][order] = [results[algo][order][depth][i][crit] for i in range(len(results[algo][order][depth]))]

    return avg_whole, avg_orders


def run_dfs(p):
    i = 0
    for puzzle in p:
    # for puzzle in ["4x4_01_00001.txt", "4x4_02_00001.txt", "4x4_03_00001.txt", "4x4_04_00001.txt", "4x4_05_00001.txt", "4x4_06_00001.txt", "4x4_07_00001.txt"]:
        for order in orders:
            dfs = DFS(search_order=order)
            dim, lay = load_config(path.join("puzzles", puzzle))
            dfs.model.load_layout(dim, lay)
            t = time()
            r = dfs.run()
            t = round((time() - t) * 1000, 3)

            depth = int(puzzle.split('_')[1])
            # print(r, puzzle, order)
            if r:
                result = {"path_length": -1, "frontier": len(dfs.frontier), "explored": len(dfs.explored), "depth": dfs.deepest, "time": t}
            else:
                result = {"path_length": len(dfs.path[0]), "frontier": len(dfs.frontier), "explored": len(dfs.explored), "depth": dfs.deepest, "time": t}

            results["DFS"][order][depth].append(result)

            print("DFS progress: {}%".format(round((i/progress) * 100, 2)), end='\r', flush=True)
            i += 1



if __name__ == "__main__":
    progress = len(puzzles) * len(orders)
    i = 0
    # for puzzle in puzzles:
    #     for order in orders:
    #         bfs = BFS(search_order=order)
    #         dim, lay = load_config(path.join("puzzles", puzzle))
    #         bfs.model.load_layout(dim, lay)
    #         t = time()
    #         r = bfs.run()
    #         t = round((time() - t) * 1000, 3)

    #         # makedirs(path.join("output", "BFS", order), exist_ok=True)
    #         # save_result(path.join("output", "BFS", order, puzzle + ".result"), bfs.path[0] if not r else [], len(bfs.path[0]) if not r else -1)

    #         # save_info(path.join("output", "BFS", order, puzzle + ".info"), len(bfs.path[0]), len(bfs.frontier), len(bfs.explored), 
    #             # len(bfs.path[0]) if not r else -1, t)


    #         # get the depth from 4x4_depth_00000.txt
    #         depth = int(puzzle.split('_')[1])
    #         result = {"path_length": len(bfs.path[0]), "frontier": len(bfs.frontier), "explored": len(bfs.explored), "depth": len(bfs.path[0]), "time": t}

    #         results["BFS"][order][depth].append(result)
            # if i % 200 == 0:
                # print("BFS progress: {}%".format(i/progress) * 100), end='\r', flush=True)
    
    # bfs_avg_whole, bfs_avg_orders = process_results("BFS")


    # i = 0
    # for puzzle in puzzles:
    # # for puzzle in ["4x4_01_00001.txt", "4x4_02_00001.txt", "4x4_03_00001.txt", "4x4_04_00001.txt", "4x4_05_00001.txt", "4x4_06_00001.txt", "4x4_07_00001.txt"]:
    #     for order in orders:
    #         dfs = DFS(search_order=order)
    #         dim, lay = load_config(path.join("puzzles", puzzle))
    #         dfs.model.load_layout(dim, lay)
    #         t = time()
    #         r = dfs.run()
    #         t = round((time() - t) * 1000, 3)

    #         depth = int(puzzle.split('_')[1])
    #         # print(r, puzzle, order)
    #         if r:
    #             result = {"path_length": -1, "frontier": len(dfs.frontier), "explored": len(dfs.explored), "depth": dfs.deepest, "time": t}
    #         else:
    #             result = {"path_length": len(dfs.path[0]), "frontier": len(dfs.frontier), "explored": len(dfs.explored), "depth": dfs.deepest, "time": t}

    #         results["DFS"][order][depth].append(result)

    #         print("DFS progress: {}%".format(round((i/progress) * 100, 2)), end='\r', flush=True)
    #         i += 1

    with ProcessPoolExecutor(max_workers=8) as executor:
        for chunk in list(chunks(puzzles, len(puzzles)//8)):
            executor.submit(run_dfs, chunk)

    dfs_avg_whole, dfs_avg_orders = process_results("DFS")    

    bar_width = 0.1
    xs = [np.arange(1, 8)]
    for i in range(1, 8):
        xs.append([x + bar_width for x in xs[i - 1]])


    # for crit in criterions:
    #     plt.xlabel("Depth")
    #     plt.title("BFS all orders")
    #     ys = []
    #     for order in orders:
    #         ys.append([mean(bfs_avg_orders[crit][i][order]) for i in range(1, 8)])
        
    #     plt.ylabel(crit.capitalize())
    #     for i in range(len(orders)):
    #         plt.bar(xs[i], ys[i], edgecolor="black", width=bar_width, label=orders[i])
    #     plt.legend()
    #     plt.savefig("bfs_orders_" + crit + ".png")
    #     plt.clf()

    for crit in criterions:
        plt.xlabel("Depth")
        plt.title("DFS all orders")
        ys = []
        for order in orders:
            ys.append([mean(dfs_avg_orders[crit][i][order]) for i in range(1, 8)])
        
        plt.ylabel(crit.capitalize())
        for i in range(len(orders)):
            plt.bar(xs[i], ys[i], edgecolor="black", width=bar_width, label=orders[i])
        plt.legend()
        plt.savefig("dfs_orders_" + crit + ".png")
        # plt.show()
        plt.clf()