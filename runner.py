import matplotlib.pyplot as plt
from bfs import BFS
from dfs import DFS
from main import load_config, save_info, save_result

from os import listdir, makedirs, path
from collections import defaultdict
from time import time
from statistics import mean


orders = ["RDUL", "RDLU", "DRUL", "DRLU", "LUDR", "LURD", "ULDR", "ULRD"]
puzzles = listdir("./puzzles")
criterions = ["path_length", "frontier", "explored", "depth", "time"]

# {alg: order: depth: criterions}
results = {key:defaultdict(dict) for key in "BFS DFS A*".split(' ')}
for foo in results:
    results[foo] = {key:defaultdict(list) for key in orders}

def process_results(algo): 
    # {criterion: depth: []}
    avg_whole = {key: defaultdict(list) for key in criterions}
    for crit in criterions:
        for l in range(1, 8):
            # bfs_avg_whole[crit][l] = mean([results["BFS"][order][l] for order in orders])
            foo = []
            for order in orders:
                foo += [results[algo][order][l][i][crit] for i in range(len(results[algo][order][l]))]
            avg_whole[crit][l] = foo
    avg_orders = {key: defaultdict(dict) for key in criterions}
    for foo in avg_orders:
        # bfs_avg_orders[foo] = {key: defaultdict for key in range(1, 8)}
        for key in range(1, 8):
            avg_orders[foo][key] = {order: list() for order in orders}

    for crit in criterions:
        for depth in avg_orders[crit]:
            foo = []
            for order in orders:
                foo += [results[algo][order][depth][i][crit] for i in range(len(results[algo][order][depth]))]
                avg_orders[crit][depth][order] = foo

    return avg_whole, avg_orders


if __name__ == "__main__":
    for puzzle in puzzles:
        for order in orders:
            bfs = BFS(search_order=order)
            dim, lay = load_config(path.join("puzzles", puzzle))
            bfs.model.load_layout(dim, lay)
            t = time()
            r = bfs.run()
            t = round((time() - t) * 1000, 3)

            # makedirs(path.join("output", "BFS", order), exist_ok=True)
            # save_result(path.join("output", "BFS", order, puzzle + ".result"), bfs.path[0] if not r else [], len(bfs.path[0]) if not r else -1)

            # save_info(path.join("output", "BFS", order, puzzle + ".info"), len(bfs.path[0]), len(bfs.frontier), len(bfs.explored), 
                # len(bfs.path[0]) if not r else -1, t)


            # get the depth from 4x4_depth_00000.txt
            depth = int(puzzle.split('_')[1])
            result = {"path_length": len(bfs.path[0]), "frontier": len(bfs.frontier), "explored": len(bfs.explored), "depth": len(bfs.path[0]), "time": t}

            results["BFS"][order][depth].append(result)
    
    bfs_avg_whole, bfs_avg_orders = process_results("BFS")

    for puzzle in "4x4_01_00001.txt 4x4_01_00002.txt".split(" "):
        for order in orders:
            dfs = DFS(search_order=order)
            dim, lay = load_config(path.join("puzzles", puzzle))
            dfs.model.load_layout(dim, lay)
            t = time()
            r = dfs.run()
            t = round((time() - t) * 1000, 3)

            depth = int(puzzle.split('_')[1])
            result = {"path_length": len(dfs.path[0]) if not r else -1, "frontier": len(dfs.frontier), "explored": len(dfs.explored), "depth": len(dfs.path[0]), "time": t}

            results["DFS"][order][depth].append(result)

    dfs_avg_whole, dfs_avg_orders = process_results("DFS")    

    plt.bar(range(1, 8), [mean(bfs_avg_whole["time"][i]) for i in range(1, 8)])
    # plt.bar([1]], [mean(dfs_avg_whole["time"][i]) for i in range(1, 8)])
    plt.bar([1], dfs_avg_whole["time"][1])
    plt.show()