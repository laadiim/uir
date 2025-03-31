from sys import argv
from typing import Dict, List

import numpy as np

USE_HEUR = True


def parse_graph(input_text):
    lines = input_text.strip().split("\n")

    start_node = lines[1]
    goal_node = lines[3]

    adjacency_list = {}
    heuristic_values = {}

    parsing_adjacency = True

    for line in lines[5:]:
        if "vzdusna vzdalenost" in line:
            parsing_adjacency = False
            continue

        if parsing_adjacency:
            node, *edges = line.split(";")
            adjacency_list[node] = {}
            for edge in edges:
                neighbor, weight = edge.split("=")
                adjacency_list[node][neighbor] = int(weight)
        else:
            node, value = line.split("=")
            heuristic_values[node.strip()] = int(value.strip())

    nodes = sorted(adjacency_list.keys())
    node_index = {node: i for i, node in enumerate(nodes)}

    matrix_size = len(nodes)
    adjacency_matrix = np.full((matrix_size, matrix_size), float("inf"))

    for node, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors.items():
            adjacency_matrix[node_index[node]][node_index[neighbor]] = weight

    np.fill_diagonal(adjacency_matrix, 0)

    heuristic_values[goal_node] = 0
    return adjacency_matrix, nodes, node_index, start_node, goal_node, heuristic_values


def search(
    adj_matrix: np.ndarray,
    node_index: Dict[str, int],
    start: str,
    goal: str,
    heuristics: Dict[str, int],
    use_heuristic: bool,
) -> List[str]:
    """Function implementing dijkstra/a* algorithm over adjacency matrix of a graph"""
    # create inverted mapping
    index_node: Dict[int, str] = {value: key for key, value in node_index.items()}
    # initialize distance at infinity
    distances: Dict[int, float] = {i: float("inf") for i in index_node.keys()}
    distances[node_index[start]] = 0  # set start distance at 0

    # initialize visited at False
    visited: Dict[int, bool] = {i: False for i in index_node.keys()}

    # initialize parents dict at None
    parents: Dict[int, int | None] = {i: None for i in index_node.keys()}

    def get_min_distance(
        distances: Dict[int, float], vistited: Dict[int, bool]
    ) -> int | None:
        """Local function finding the unvisited vertex with lowest distance"""
        min_index: int | None = None
        min_value: float = float("inf")
        for i in distances.keys():
            if not visited[i] and min_index != i and distances[i] < min_value:
                min_index = i
                min_value = distances[i]
        return min_index

    # ======================================================================================

    # initialize current at start node
    curr: int | None = node_index[start]

    # iterate until reaching goal node
    while curr is not None and curr != node_index[goal]:
        visited[curr] = True

        # iterate over row in the matrix, update distances and parents
        for j in range(len(adj_matrix[curr])):
            weigth: float = distances[curr] + adj_matrix[curr, j]
            if (
                j != curr
                and not visited[j]
                and distances[j]
                > weigth + (heuristics[index_node[j]] if use_heuristic else 0)
            ):
                distances[j] = weigth
                parents[j] = curr

        # get next current
        curr = get_min_distance(distances, visited)

    # initialize empty path
    path: List[str] = []

    # backtrack to recreate path
    while curr is not None:
        path.append(index_node[curr])
        curr = parents[curr]

    # reverse path to have it start with start
    path.reverse()
    print(distances[node_index[goal]])
    return path


def main():
    input_text: str = ""
    with open(argv[1], "r") as file:
        input_text = file.read()

    adj_matrix, _, node_index, start, goal, heuristics = parse_graph(input_text)
    """
    print("Adjacency Matrix:")
    print(adj_matrix)
    print("\nNode Index Mapping:", node_index)
    print("\nStart Node:", start)
    print("Goal Node:", goal)
    print("\nHeuristic Values:", heuristics)
    """
    print(search(adj_matrix, node_index, start, goal, heuristics, USE_HEUR))


if __name__ == "__main__":
    main()
