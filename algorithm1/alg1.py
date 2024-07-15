import sys

from algorithm1.Network import Network

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

                network = Network()
                network.generate_random_graph(num_nodes=10, probability=0.1, num_paths=num_paths)

                print(network.algorithm1())

                network.draw_graph()
                pass
            case '2':
                network = Network()
                network.generate_paper_graph()
                print(network.algorithm1())

                # Arrange the graph as presented in the paper
                pos = {
                    "S": (0, 1),
                    2: (1, 2),
                    3: (1, 1),
                    4: (1, 0),
                    5: (2, 1),
                    6: (3, 2),
                    7: (3, 0),
                    "T": (4, 1)
                }

                network.draw_graph(position=pos)
            case '3':
                pass
            case '4':
                pass
            case '5':
                pass
            case '6':
                sys.exit()

