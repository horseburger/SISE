from bfs import BFS
import argparse




# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="Choose between bfs, dfs and astr", choices=["bfs", "dfs", "astr"])
parser.add_argument("parameter", help="Choose the search order (LRUD) or the heurictic (hamm, manh)")
parser.add_argument("start", help="File name with the starting order of the puzzle")
parser.add_argument("output", help="Result filename")
parser.add_argument("info", help="Additional info filename")

args = parser.parse_args()


if __name__ == "__main__":
    bfs = BFS()

    bfs.start()