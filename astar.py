 import numpy as np

def parse_graph(input_text):
    lines = input_text.strip().split('\n')
    
    start_node = lines[0].split(':')[1].strip()
    goal_node = lines[1].split(':')[1].strip()
    
    adjacency_list = {}
    heuristic_values = {}
    
    parsing_adjacency = True
    
    for line in lines[2:]:
        if 'vzdusna vzdalenost' in line:
            parsing_adjacency = False
            continue
        
        if parsing_adjacency:
            node, *edges = line.split(';')
            adjacency_list[node] = {}
            for edge in edges:
                neighbor, weight = edge.split('=')
                adjacency_list[node][neighbor] = int(weight)
        else:
            node, value = line.split('=')
            heuristic_values[node.strip()] = int(value.strip())
    
    nodes = sorted(adjacency_list.keys())
    node_index = {node: i for i, node in enumerate(nodes)}
    
    matrix_size = len(nodes)
    adjacency_matrix = np.full((matrix_size, matrix_size), float('inf'))
    
    for node, neighbors in adjacency_list.items():
        for neighbor, weight in neighbors.items():
            adjacency_matrix[node_index[node]][node_index[neighbor]] = weight
    
    np.fill_diagonal(adjacency_matrix, 0)
    
    return adjacency_matrix, nodes, node_index, start_node, goal_node, heuristic_values

input_text = """start:
S
cil:
G
seznam sousednosti:
A;S=36;C=13;G=43
B;S=11;C=31
C;A=13;B=31;G=19
S;A=36;B=11
G;A=43;C=19
vzdusna vzdalenost od cile:
A=26
B=47
C=14
S=52"""

adj_matrix, nodes, node_index, start, goal, heuristics = parse_graph(input_text)
print("Adjacency Matrix:")
print(adj_matrix)
print("\nNode Index Mapping:", node_index)
print("\nStart Node:", start)
print("Goal Node:", goal)
print("\nHeuristic Values:", heuristics)
