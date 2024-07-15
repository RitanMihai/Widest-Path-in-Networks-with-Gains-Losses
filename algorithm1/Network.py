import math
import random

import networkx as nx
from matplotlib import pyplot as plt


class Network:
    def __init__(self):
        self.graph = None
        self.source = None
        self.sink = None

    # TODO: Take in consideration to add Cycles
    def generate_random_graph(self, num_nodes, probability=0.5, num_paths=2):
        """
        :param num_nodes: Total number of paths
        :param probability: Probability of generate an arc
        :param num_paths: Add paths from source to sink.
                          Can add new arcs in order to build a valid directed path.
                          The number of arcs exiting the source would be 1 <= source out <= num_paths
                          The number of arcs entering the sink would be 1 <= sink in <= num_paths
        :return: void
        """
        if num_paths < 1:
            raise ValueError("Invalid number of paths given! There should be at least one valid path")

        # https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.erdos_renyi_graph.html
        self.graph = nx.erdos_renyi_graph(n=num_nodes-2, p=probability, directed=True)

        self.source = "S"
        self.sink = "T"

        self.graph.add_node(self.source)
        self.graph.add_node(self.sink)

        # Generate paths from Source to Sink
        for i in range(num_paths):
            # TODO: Analyze the option to generate paths from one node to n-1
            #   In the current state is always n-2: S (n_1) -> [n_2, n_3, ... n_n-1] -> T (n)
            #   Propose, select a rand_n random number of elements and build path: S (n_1) -> [rand_n] -> T (n)

            nodes = list(self.graph.nodes)
            nodes.remove(self.source)
            nodes.remove(self.sink)
            random.shuffle(nodes)

            # Connect Source and Sink
            path_nodes = [self.source] + nodes + [self.sink]
            for j in range(len(path_nodes)-1):
                self.graph.add_edge(path_nodes[j], path_nodes[j+1])

        # Generate Random Capacities and losses
        for u, v in self.graph.edges():
            self.graph[u][v]['capacity'] = random.randint(1, 10)  # Random capacity between 1 and 10
            self.graph[u][v]['loss'] = random.uniform(0.1, 0.99)  # Random loss between 0.1 and 1.0

    def generate_custom_graph(self):
        # TODO: Offer user the option to add it's own data
        pass

    def generate_paper_graph(self):
        self.graph = nx.DiGraph()

        edges = [
            ("S", 2, {'capacity': 7, 'loss': 0.86}),
            ("S", 3, {'capacity': 8, 'loss': 0.73}),
            ("S", 4, {'capacity': 10, 'loss': 0.82}),
            (2, 3, {'capacity': 6, 'loss': 0.8}),
            (2, 5, {'capacity': 10, 'loss': 0.74}),
            (3, 2, {'capacity': 5, 'loss': 0.9}),
            (3, 4, {'capacity': 6, 'loss': 0.7}),
            (3, 5, {'capacity': 3, 'loss': 0.89}),
            (4, 3, {'capacity': 5, 'loss': 0.9}),
            (4, 5, {'capacity': 13, 'loss': 0.68}),
            (5, 6, {'capacity': 1, 'loss': 0.9}),
            (5, 7, {'capacity': 8, 'loss': 0.2}),
            (5, "T", {'capacity': 4, 'loss': 0.5}),
            (6, "T", {'capacity': 3, 'loss': 0.89}),
            (7, "T", {'capacity': 9, 'loss': 0.3}),
        ]

        self.graph.add_edges_from(edges)
        self.source = "S"
        self.sink = "T"

    def draw_graph(self, position=None):
        pos = nx.spring_layout(self.graph)

        if pos is not None:
            pos = position

        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)

        # Draw edge labels for capacities and lengths
        edge_labels = {(u, v): f"{d['capacity']} l={d['length']:.2f}" for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        # Draw edge labels for losses
        loss_labels = {(u, v): f"loss={d['loss']}" for u, v, d in self.graph.edges(data=True)}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=loss_labels, label_pos=0.3, font_color='red')

        plt.show()

    def algorithm1(self):
        for u, v, data in self.graph.edges(data=True):
            if u == self.source:
                data['length'] = -math.log(data['loss'] * data['capacity'])
            else:
                data['length'] = -math.log(data['loss'])

        while True:
            sp = nx.shortest_path(self.graph, source=self.source, target=self.sink, weight='length')

            # Most Saturated Arc
            capacities = {(u, v): self.graph[u][v]['capacity'] for u, v in zip(sp[:-1], sp[1:])}
            saturated_arc = min(capacities, key=capacities.get)

            if saturated_arc[0] == self.source:
                # Combine the stored path on the artificial arc with the rest of the path
                stored_path = self.graph[saturated_arc[0]][saturated_arc[1]].get('path_so_far', [])
                full_path = stored_path + sp[sp.index(saturated_arc[1]) + 1:]
                return full_path
            else:
                u, v = saturated_arc
                artificial_arc = -math.log(self.graph[u][v]['capacity'] * self.graph[u][v]['loss'])
                self.graph.add_edge(self.source, v, length=artificial_arc, capacity=self.graph[u][v]['capacity'], loss=self.graph[u][v]['loss'],
                           path_so_far=sp[:sp.index(v) + 1])
                self.graph.remove_edge(u, v)