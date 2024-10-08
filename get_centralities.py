import yaml
import networkx as nx

GRAPH_FILENAME = 'fofoc.yaml'
TARGET_IDS = [202377873, 210835290]

def load_graph(filename):
    """Загрузка графа из YAML файла"""
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        # Построение графа из данных
        G = nx.Graph()
        # Добавление узлов
        for node in data['nodes']:
            G.add_node(node['id'])
        # Добавление рёбер
        for link in data['links']:
            G.add_edge(link['source'], link['target'])
        return G

def calculate_centralities(graph, target_ids):
    """Вычисление центральностей для указанных вершин"""
    # Центральность по посредничеству
    betweenness = nx.betweenness_centrality(graph)
    # Центральность по близости
    closeness = nx.closeness_centrality(graph)

    # Извлечение значений для целевых вершин
    results = {}
    for node_id in target_ids:
        results[node_id] = {
            'betweenness_centrality': betweenness.get(node_id, 0),
            'closeness_centrality': closeness.get(node_id, 0),
        }

    return results

def main():
    # Загружаем граф
    graph = load_graph(GRAPH_FILENAME)

    # Рассчитываем центральности для целевых вершин
    centralities = calculate_centralities(graph, TARGET_IDS)

    # Выводим результаты
    for node_id, values in centralities.items():
        print(f"Node ID: {node_id}")
        print(f"  Betweenness Centrality: {values['betweenness_centrality']}")
        print(f"  Closeness Centrality: {values['closeness_centrality']}")

if __name__ == "__main__":
    main()
