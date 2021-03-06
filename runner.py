import matplotlib.pyplot as plt
from bfs import BFS
from dfs import DFS
from astr import ASTR
from main import load_config, save_info, save_result

from os import listdir, makedirs
import os
from collections import defaultdict
from time import time
from statistics import mean
import numpy as np
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import json


orders = ["RDUL", "RDLU", "DRUL", "DRLU", "LUDR", "LURD", "ULDR", "ULRD"]
puzzles = listdir("./puzzles")
criterions = ["path_length", "frontier", "explored", "depth", "time"]
algos = ["BFS", "DFS", "A*"]
# heuristics = ["hamm", "manh"]
heuristics = ["hamm", "manh"]

# # {alg: order: depth: criterions}
# results = {key:defaultdict(dict) for key in "BFS DFS A*".split(' ')}
# for foo in results:
#     results[foo] = {key:defaultdict(list) for key in orders}


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def init_results():
    # {alg: order: depth: criterions}
    results = {key:defaultdict(dict) for key in algos}
    for foo in results:
        if foo == "A*":
            results[foo] = {key: defaultdict(list) for key in heuristics}
        else:
            results[foo] = {key:defaultdict(list) for key in orders}
    return results


def process_results(algo, results):
    # {criterion: depth: []}
    vars = heuristics if algo == "A*" else orders
    avg_whole = {key: defaultdict(list) for key in criterions}
    for crit in criterions:
        for order in vars:
            foo = []
            for l in results[algo][order].keys():
                avg_whole[crit][l] = [results[algo][order][l][i][crit] for i in range(len(results[algo][order][l]))]
            # avg_whole[crit][l] = foo
    # {criterion: depth: order: }
    avg_orders = {key: defaultdict(dict) for key in criterions}
    for foo in avg_orders:
        # get the depth values
        bar = list(results[algo].items())[0][0]
        for key in results[algo][bar].keys():
            avg_orders[foo][key] = {order: list() for order in vars}

    for crit in criterions:
        for depth in avg_orders[crit]:
            for order in vars:
                avg_orders[crit][depth][order] = [results[algo][order][depth][i][crit] for i in range(len(results[algo][order][depth]))]

    return avg_whole, avg_orders

def merge_results(_results, algo):
    final = init_results()
    loop = heuristics if algo == "A*" else orders
    for res in _results:
        for l in loop:
            for depth in res[algo][l]:
                final[algo][l][depth] += res[algo][l][depth]
    
    return final
                
def get_dfs_results(_results):
    return process_results("DFS", merge_results(_results, "DFS"))

def run_dfs(p):
    results = init_results()

    i = 0
    progress = len(p) * 8
    for puzzle in p:
    # for puzzle in ["4x4_01_00001.txt", "4x4_02_00001.txt", "4x4_03_00001.txt", "4x4_04_00001.txt", "4x4_05_00001.txt", "4x4_06_00001.txt", "4x4_07_00001.txt"]:
        for order in orders:
            dfs = DFS(search_order=order)
            dim, lay = load_config(os.path.join("puzzles", puzzle))
            dfs.model.load_layout(dim, lay)
            t = time()
            path = dfs.run()
            t = round((time() - t) * 1000, 3)

            depth = int(puzzle.split('_')[1])
            # print(r, puzzle, order)
            if path == -1:
                continue

            result = {"path_length": len(path), "frontier": len(dfs.frontier) + len(dfs.explored), "explored": len(dfs.explored), "depth": dfs.deepest, "time": t}

            results["DFS"][order][depth].append(result)

            print("DFS progress: {}%".format(round((i/progress) * 100, 2)), end='\r', flush=True)
            i += 1
    return results

def run_bfs(p):
    results = init_results()
    progress = len(puzzles) * len(orders)
    i = 0
    for puzzle in puzzles:
        for order in orders:
            bfs = BFS(search_order=order)
            dim, lay = load_config(os.path.join("puzzles", puzzle))
            bfs.model.load_layout(dim, lay)
            t = time()
            path = bfs.run()
            t = round((time() - t) * 1000, 3)

            # get the depth from 4x4_depth_00000.txt
            depth = int(puzzle.split('_')[1])
            if path == -1:
                continue

            result = {"path_length": len(path), "frontier": len(bfs.frontier) + len(bfs.explored), "explored": len(bfs.explored), "depth": len(path), "time": t}

            results["BFS"][order][depth].append(result)
            print("BFS progress: {}%".format(round((i/progress) * 100, 2)), end='\r', flush=True)
            i += 1
    
    # avg_whole, avg_orders
    return process_results("BFS", results)

def run_astr(p):
    results = init_results()
    progress = len(puzzles) * len(heuristics)
    i = 0
    for puzzle in puzzles:
        for heur in heuristics:
            astr = ASTR(search_strategy=heur)
            dim, lay = load_config(os.path.join("puzzles", puzzle))
            astr.model.load_layout(dim, lay)
            t = time()
            path = astr.run()
            t = round((time() - t) * 1000, 3)

            # get the depth from 4x4_depth_00000.txt
            depth = int(puzzle.split('_')[1])
            if path == -1:
                continue

            result = {"path_length": len(path), "frontier": len(astr.frontier) + len(astr.explored), "explored": len(astr.explored), "depth": len(path), "time": t}

            results["A*"][heur][depth].append(result)
            print("A* progress: {}%".format(round((i/progress) * 100, 2)), end='\r', flush=True)
            i += 1
    
    # avg_whole, avg_orders
    return process_results("A*", results)

if __name__ == "__main__":
    print("# Running BFS...")
    t = time()
    bfs_avg_whole, bfs_avg_orders = run_bfs(puzzles)
    print("# BFS done in: {}s\n".format(round(time() - t, 3)))

    with open("bfs_avg_whole.out", 'w') as f:
        json.dump(bfs_avg_whole, f)
    with open("bfs_avg_order.out", 'w') as f:
        json.dump(bfs_avg_orders, f)

    print("# Running DFS...")
    jobs = []
    foo = time()
    with ProcessPoolExecutor(max_workers=15) as executor:
        for chunk in list(chunks(puzzles, len(puzzles)//15)):
            jobs.append(executor.submit(run_dfs, chunk))
    print("# DFS done in: {}s\n".format(round(time() - foo, 3)))
    res = [i.result() for i in jobs]



    dfs_avg_whole, dfs_avg_orders = get_dfs_results(res)  

    with open("dfs_avg_whole.out", 'w') as f:
        json.dump(dfs_avg_whole, f)
    with open("dfs_avg_orders.out", 'w') as f:
        json.dump(dfs_avg_orders, f)

    print("# Running A*...")
    t = time()
    astr_avg_whole, astr_avg_orders = run_astr(puzzles)
    print("# A* done in: {}s\n".format(round(time() - t, 3)))


    bar_width = 0.1
    xs = [np.arange(1, len(orders))]
    for i in range(1, len(orders)):
        xs.append([x + bar_width for x in xs[i - 1]])


    print("# Plotting BFS...")

    for crit in criterions:
        plt.xlabel("Depth")
        plt.title("BFS all orders")
        ys = []
        for order in orders:
            ys.append([mean(bfs_avg_orders[crit][i][order]) for i in sorted(bfs_avg_orders[crit].keys())])
        
        plt.ylabel(crit.capitalize())
        for i in range(len(orders)):
            plt.bar(xs[i], ys[i], edgecolor="black", width=bar_width, label=orders[i])
        plt.legend()
        plt.savefig("bfs_orders_" + crit + ".png")
        # plt.show()
        plt.clf()

    print("# Plotting DFS...")

    for crit in criterions:
        plt.xlabel("Depth")
        plt.title("DFS all orders")
        ys = []

        if crit == "explored" or crit == "frontier" or crit == "time":
            plt.yscale("log")

        for order in orders:
            ys.append([mean(dfs_avg_orders[crit][i][order]) for i in sorted(dfs_avg_orders[crit].keys())])
        

        plt.ylabel(crit.capitalize())
        for i in range(len(orders)):
            plt.bar(xs[i], ys[i], edgecolor="black", width=bar_width, label=orders[i])
        plt.legend()
        plt.savefig("dfs_orders_" + crit + ".png")
        # plt.show()
        plt.clf()

    print("# Plotting A*...")
    for crit in criterions:
        plt.xlabel("Depth")
        plt.title("A* all orders")
        ys = []

        # if crit == "explored" or crit == "frontier" or crit == "time":
        #     plt.yscale("log")

        for heur in heuristics:
            ys.append([mean(astr_avg_orders[crit][i][heur]) for i in sorted(astr_avg_orders[crit].keys())])
        

        plt.ylabel(crit.capitalize())
        for i in range(len(heuristics)):
            plt.bar(xs[i], ys[i], edgecolor="black", width=bar_width, label=heuristics[i])
        plt.legend()
        plt.savefig("astr_" + crit + ".png")
        # plt.show()
        plt.clf()

    print("# Plotting all...")


    xs = [np.arange(1, 8)]
    for i in range(1, 4):
        xs.append([x + bar_width for x in xs[i - 1]])


    for crit in criterions:
        plt.xlabel("Depth")
        plt.title("All algos average")
        ys = {key: list() for key in algos}
        if crit == "explored" or crit == "frontier" or crit == "time":
            plt.yscale("log")

        ys["BFS"] = [mean(bfs_avg_whole[crit][depth]) for depth in sorted(bfs_avg_whole[crit])]
        ys["DFS"] = [mean(dfs_avg_whole[crit][depth]) for depth in sorted(dfs_avg_whole[crit])]
        ys["A*"] = [mean(astr_avg_whole[crit][depth]) for depth in sorted(astr_avg_whole[crit])]

        plt.ylabel(crit.capitalize())
        plt.bar(xs[0], ys["BFS"], edgecolor="black", width=bar_width, label="BFS")
        plt.bar(xs[1], ys["DFS"], edgecolor="black", width=bar_width, label="DFS")
        plt.bar(xs[2], ys["A*"], edgecolor="black", width=bar_width, label="A*")
        plt.legend()
        # plt.show()
        plt.savefig("all_" + crit + ".png")
        plt.clf()