from itertools import permutations
from typing import List
import networkx as nx

from utils.utils import run_parts


testInput = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""

def get_all_distances(input_lines: List[str]):
    G = nx.Graph()
    for line in input_lines:
        locations, distance = line.split(" = ")
        source, destination = locations.split(" to ")
        G.add_edge(source, destination, distance=int(distance))

    """Find all possible path distances that visit every location once."""
    all_dist = set()
    for path in permutations(G.nodes):
        dist = 0
        for a, b in zip(path, path[1:]):
            dist += G.get_edge_data(a, b)["distance"]
        all_dist.add(dist)
    return all_dist

def part1(input_lines: List[str]):
    return min(get_all_distances(input_lines))


def part2(input_lines: List[str]):
    return max(get_all_distances(input_lines))

if __name__ == "__main__":
    # print(part1(testInput.splitlines()))
    run_parts(part1, part2, 2015, 9)
