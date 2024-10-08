import yaml
import networkx as nx

GRAPH_FILENAME = 'fofoc.yaml'
TARGET_IDS = [202377873, 210835290]

def load_graph(filename):
    """Загрузка графа из YAML файла"""
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        G = nx.Graph()
        for node in data['nodes']:
            G.add_node(node['id'])
        for link in data['links']:
            G.add_edge(link['source'], link['target'])
        return G

def calculate_centralities(graph, target_ids):
    """Вычисление центральностей для указанных вершин"""
    betweenness = nx.betweenness_centrality(graph)
    closeness = nx.closeness_centrality(graph)

    results = {}
    for node_id in target_ids:
        results[node_id] = {
            'betweenness_centrality': betweenness.get(node_id, 0),
            'closeness_centrality': closeness.get(node_id, 0),
        }

    return results

def main():
    graph = load_graph(GRAPH_FILENAME)

    centralities = calculate_centralities(graph, TARGET_IDS)

    for node_id, values in centralities.items():
        print(f"Node ID: {node_id}")
        print(f"  Betweenness Centrality: {values['betweenness_centrality']}")
        print(f"  Closeness Centrality: {values['closeness_centrality']}")

if __name__ == "__main__":
    main()
