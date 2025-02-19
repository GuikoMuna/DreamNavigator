import json
import networkx as nx
from collections import deque

def build_graph_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    graph = nx.DiGraph()

    for connection in data.get("connections", []):
        origin = connection["origin"]
        destination = connection["destination"]
        attributes = connection.get("attributes", [])
        unlock_condition = connection.get("unlockCondition", None)
        is_removed = connection.get("isRemoved", False)
        effects_needed = connection.get("effectsNeeded", [])
        chance_percentage = connection.get("chancePercentage", None)
        chance_description = connection.get("chanceDescription", None)
        season_available = connection.get("seasonAvailable", None)

        graph.add_edge(
            origin, 
            destination, 
            attributes=attributes, 
            unlock_condition=unlock_condition, 
            is_removed=is_removed, 
            effects_needed=effects_needed,
            chance_percentage=chance_percentage,
            chance_description=chance_description,
            season_available=season_available
        )

    return graph

def show_basic_info(graph):
    total_nodes = graph.number_of_nodes()
    total_edges = graph.number_of_edges()
    print(f"N Nodes: {total_nodes}")
    print(f"N Edges: {total_edges}")

def remove_removeds(graph):
    edges_to_remove = []

    for u, v, data in graph.edges(data=True):
        if data.get("is_removed", False):
            edges_to_remove.append((u, v))

    graph.remove_edges_from(edges_to_remove)

    nodes_to_remove = [node for node in graph.nodes() if graph.degree(node) == 0]
    graph.remove_nodes_from(nodes_to_remove)

def find_longest_path(graph, start_node):
    longest_path = []


    def dfs(node, visited, current_path):
        nonlocal longest_path

        visited.add(node)
        current_path.append(node)

        if len(current_path) > len(longest_path):
            longest_path = current_path.copy()

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor, visited, current_path)

        visited.remove(node)
        current_path.pop()

    dfs(start_node, set(), [])

    print(longest_path)

def bfs_deepest_nodes(graph, start_node):

    queue = deque([(start_node, 0)])
    visited = {start_node}
    max_depth = 0
    deepest_nodes = []
    
    while queue:
        node, depth = queue.popleft()
        

        if depth > max_depth:
            max_depth = depth
            deepest_nodes = [node]
        elif depth == max_depth:
            deepest_nodes.append(node)
        
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                queue.append((neighbor, depth + 1))
                visited.add(neighbor)
    
    print(f"Deepest of limit {max_depth}: {deepest_nodes}")

file_path = r'C:\Repos\DreamGPS\yume.json' #change
startingPoint = "Nexus" #change

graph = build_graph_from_json(file_path)

remove_removeds(graph)
find_longest_path(graph,startingPoint) 