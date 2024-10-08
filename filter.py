import yaml
import networkx as nx
import os

GRAPH_FILENAME = 'fofoc.yaml'
FILTERED_GRAPH_FILENAME = 'fofoc-filtered.yaml'
VK_IDS = [
    202377873,
    210835290
]


def save_graph(graph, filename):
    with open(filename, 'w') as file:
        yaml.dump(nx.node_link_data(graph), file)


def load_graph(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
            return nx.node_link_graph(data)
    return nx.Graph()


def filter_graph(graph):
    nodes_to_remove = [node for node in graph.nodes if graph.degree(node) <= 1 and node not in VK_IDS]
    graph.remove_nodes_from(nodes_to_remove)


def main():
    friends_graph = load_graph(GRAPH_FILENAME)

    filter_graph(friends_graph)

    save_graph(friends_graph, FILTERED_GRAPH_FILENAME)

    print(f"Number of nodes after filtering: {friends_graph.number_of_nodes()}")

if __name__ == "__main__":
    main()
