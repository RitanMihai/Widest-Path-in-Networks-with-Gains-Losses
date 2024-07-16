import json
import sys
import time

from matplotlib import pyplot as plt

from network import Network


def run_experiments():
    """ Original paper:
        | ID | No. of Instances | No. Nodes | No. of Paths | Erdős–Rényi Prob. |
        |----|------------------|-----------|--------------|-------------------|
        | 1  |        10000     |    1000   |     10     |       0.5         |
        | 2  |        10000     |    1000   |     10     |       0.7         |
        | 3  |        10000     |    1000   |     10     |       0.9         |
        | 4  |        1000      |    2000   |     10     |       0.1         |
        | 5  |        1000      |    2000   |     10     |       0.15        |
        | 6  |        1000      |    2000   |     10     |       0.6         |
        | 7  |        1000      |    2000   |     10     |       0.6         |
        | 8  |        100       |    5000   |     10     |       0.1         |
        | 9  |        100       |    5000   |     10     |       0.2         |
        | 10 |        100       |    5000   |     10     |       0.3         |
        | 11 |        5         |   10000   |     10     |       0.15        |
        | 12 |        5         |   10000   |     10     |       0.3         |
        | 13 |        5         |   10000   |     10     |       0.5         |
        | 14 |        3         |   15000   |     10     |       0.15        |
        | 15 |        2         |   20000   |     10     |       0.15        |
        | 16 |        1         |   25000   |     10     |       0.15        |
    """

    experiment_configs = [
        (1,  1000, 10, 0.5),
        (1,  1000, 10, 0.7),
        (1,  1000, 10, 0.9),
        (1,  2000, 10, 0.1),
        (1,  2000, 10, 0.15),
        (1,  2000, 10, 0.6),
        (1,  2000, 10, 0.6),
        (1,  5000, 10, 0.1),
        (1,  5000, 10, 0.2),
        (1,  5000, 10, 0.3),
        (1, 10000, 10, 0.15),
        (1, 10000, 10, 0.3),
        (1, 10000, 10, 0.5),
        (1, 15000, 10, 0.15),
        (1, 20000, 10, 0.15),
        (1, 25000, 10, 0.15),
    ]

    results = []

    for no_of_instances, no_nodes, no_paths, prob in experiment_configs:
        times = []
        edges = []
        for i in range(no_of_instances):
            network = Network()
            network.generate_random_graph(num_nodes=no_nodes, probability=prob, num_paths=no_paths, is_fast_generator=True)

            start_time = time.perf_counter()
            network.algorithm1_parallel()
            end_time = time.perf_counter()
            total_time = end_time - start_time

            times.append(total_time)
            edges.append(len(network.graph.edges))
            print(f"Experiment {i+1}/{no_of_instances} for config (nodes: {no_nodes}, paths: {no_paths}, edges: {len(network.graph.edges)}, prob: {prob}) - Time: {total_time}s")

        average_time = sum(times) / no_of_instances
        average_edges = sum(edges) / no_of_instances

        results.append({
            "nodes": no_nodes,
            "paths": no_paths,
            "avg_edges": average_edges,
            "average_time": average_time,
            "probability": prob
        })

    with open('stats.json', 'w') as f:
        json.dump(results, f, indent=4)

def plot_performance_tests():
    try:
        with open('stats.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("No performance test results found. Please run the experiments first.")
        return

    nodes = [result['nodes'] for result in results]
    paths = [result['paths'] for result in results]
    times = [result['average_time'] for result in results]
    probabilities = [result['probability'] for result in results]

    fig, ax = plt.subplots()
    scatter = ax.scatter(nodes, times, c=probabilities, cmap='viridis', alpha=0.7, edgecolors='w', linewidth=0.5)

    # Create a color bar
    cbar = plt.colorbar(scatter)
    cbar.set_label('Erdős–Rényi Probability')

    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Average Time (s)')
    ax.set_title('Performance Tests: Nodes vs Average Time')

    plt.show()

def main_menu():
    print("Select an option:")
    print("1. Generate a RANDOM GRAPH;")
    print("2. Run paper example;")
    print("3. Run performance tests;")
    print("4. Plot performance tests;")
    print("5. Show step by step algorithm (Example From Paper);")
    print("6. Exit;")

    choice = input("Enter your choice: ")
    return choice


if __name__ == '__main__':

    while True:
        choice = main_menu()
        match choice:
            case '1':
                num_nodes = int(input("Insert number of nodes: "))
                probability = float(input("Insert probability (values from 0.1 to 1.0): "))
                num_paths = int(input("Insert number of paths (values >= 1): "))

                start_time_gen = time.perf_counter()
                network = Network()
                network.generate_random_graph(num_nodes=num_nodes, probability=probability, num_paths=num_paths)
                end_time_gen = time.perf_counter()
                total_time_gen = end_time_gen - start_time_gen
                print(f"Time to generate:{total_time_gen}")

                start_time = time.perf_counter()
                print(f"Alg1 path: {network.algorithm1_parallel()}")
                end_time = time.perf_counter()
                total_time = end_time - start_time
                print(f"Alg. time:{total_time_gen}")
            case '2':
                network = Network()
                network.generate_paper_graph()
                print(network.algorithm1())
                # Arrange the graph as presented in the paper
                #pos = {
                #    "S": (0, 1),
                #    2: (1, 2),
                #    3: (1, 1),
                #    4: (1, 0),
                #    5: (2, 1),
                #    6: (3, 2),
                #    7: (3, 0),
                #    "T": (4, 1)
                #}

                #network.draw_graph(position=pos)
            case '3':
                run_experiments()
            case '4':
                plot_performance_tests()
            case '5':
                pass
            case '6':
                sys.exit()
