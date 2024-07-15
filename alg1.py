import networkx as nx
import matplotlib.pyplot as plt
import math


# Function to find the shortest path with respect to length
def find_shortest_path_length(G, source, sink):
    return nx.shortest_path(G, source=source, target=sink, weight='length')


# Function to find the most saturated arc in a given path
def find_most_saturated_arc(G, path):
    capacities = {(u, v): G[u][v]['capacity'] for u, v in zip(path[:-1], path[1:])}
    return min(capacities, key=capacities.get), min(capacities.values())


# Function to modify the graph based on the saturated arc
def modify_graph(G, path, saturated_arc):
    u, v = saturated_arc
    artificial_arc = -math.log(G[u][v]['capacity'] * G[u][v]['loss'])
    G.add_edge(source, v, length=artificial_arc, capacity=G[u][v]['capacity'], loss=G[u][v]['loss'],
               path_so_far=path[:path.index(v) + 1])
    G.remove_edge(u, v)


def gwpp(G, source, sink):
    while True:
        # Find the shortest path
        path = find_shortest_path_length(G, source, sink)
        print(f"Shortest path: {path}")

        # Find the most saturated arc
        saturated_arc, _ = find_most_saturated_arc(G, path)
        print(f"Saturated arc: {saturated_arc}")

        # Check if the saturated arc starts from the source
        if saturated_arc[0] == source:
            # Combine the stored path on the artificial arc with the rest of the path
            stored_path = G[saturated_arc[0]][saturated_arc[1]].get('path_so_far', [])
            full_path = stored_path + path[path.index(saturated_arc[1]) + 1:]
            print(f"Final shortest path: {full_path}")
            break
        else:
            # Modify the graph
            modify_graph(G, path, saturated_arc)


if __name__ == '__main__':
    # Step 1: Create a directed graph
    G = nx.DiGraph()

    # Step 2: Add edges with capacities, losses, and initialize flows and weights
    edges = [
        (1, 2, {'capacity': 7, 'loss': 0.86}),
        (1, 3, {'capacity': 8, 'loss': 0.73}),
        (1, 4, {'capacity': 10, 'loss': 0.82}),
        (2, 3, {'capacity': 6, 'loss': 0.8}),
        (2, 5, {'capacity': 10, 'loss': 0.74}),
        (3, 2, {'capacity': 5, 'loss': 0.9}),
        (3, 4, {'capacity': 6, 'loss': 0.7}),
        (3, 5, {'capacity': 3, 'loss': 0.89}),
        (4, 3, {'capacity': 5, 'loss': 0.9}),
        (4, 5, {'capacity': 13, 'loss': 0.68}),
        (5, 6, {'capacity': 1, 'loss': 0.9}),
        (5, 7, {'capacity': 8, 'loss': 0.2}),
        (5, 8, {'capacity': 4, 'loss': 0.5}),
        (6, 8, {'capacity': 3, 'loss': 0.89}),
        (7, 8, {'capacity': 9, 'loss': 0.3})
    ]

    # Add edges to the graph
    G.add_edges_from(edges)

    # Step 3: Initialize the lengths
    source = 1
    sink = 8

    for u, v, data in G.edges(data=True):
        if u == source:
            data['length'] = -math.log(data['loss'] * data['capacity'])
        else:
            data['length'] = -math.log(data['loss'])

    gwpp(G, source, sink)

    # Draw the graph
    pos = {
        1: (0, 1),
        2: (1, 2),
        3: (1, 1),
        4: (1, 0),
        5: (2, 1),
        6: (3, 2),
        7: (3, 0),
        8: (4, 1)
    }

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold',
            arrows=True)

    # Draw edge labels for capacities and weights
    edge_labels = {(u, v): f"{d['capacity']} l={d['length']:.2f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Draw edge labels for losses
    loss_labels = {(u, v): f"loss={d['loss']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=loss_labels, label_pos=0.3, font_color='red')

    plt.show()
