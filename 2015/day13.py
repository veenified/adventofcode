from itertools import permutations
from utils.utils import run_parts
from networkx import Graph, max_weight_matching
import re


test_input = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""


def parse_input_into_graph(input_lines: list[str]):
    G = Graph()
    pattern = r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)"

    for line in input_lines:
        subject, action, units, neighbor = re.match(pattern, line).groups()
        units = int(units) if action == "gain" else -int(units)

        # If edge exists, add to existing weight, otherwise create new edge
        if G.has_edge(subject, neighbor):
            G[subject][neighbor]["weight"] += units
        else:
            G.add_edge(subject, neighbor, weight=units)

    return G


def find_max_happiness(G: Graph):
    max_happiness = float("-inf")
    max_path = []
    for path in permutations(G.nodes):
        happiness = 0
        for a, b in zip(path, path[1:]):
            happiness += G[a][b]["weight"]
        happiness += G[path[0]][path[-1]]["weight"]
        if happiness > max_happiness:
            max_happiness = happiness
            max_path = path
    return max_happiness, max_path


def part1(input_lines: list[str]):
    G = parse_input_into_graph(input_lines)
    max_happiness, max_path = find_max_happiness(G)
    print(f"Total Happiness: {max_happiness}")
    return max_happiness


def part2(input_lines: list[str]):
    G = parse_input_into_graph(input_lines)
    G.add_node("Me")
    for node in list(G.nodes())[:-1]:  # Exclude "Me" which was just added
        G.add_edge("Me", node, weight=0)
        G.add_edge(node, "Me", weight=0)
    max_happiness, max_path = find_max_happiness(G)
    print(f"Total Happiness: {max_happiness}")
    return max_happiness


if __name__ == "__main__":
    # print(part1(test_input.split("\n")))
    run_parts(part1, part2, 2015, 13)
