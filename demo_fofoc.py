import yaml
import networkx as nx
import matplotlib.pyplot as plt

GRAPH_FILENAME = 'friends-of-friends-of-colleagues.yaml'

id_to_name = {
    225790978: "Владислав",
    752279211: "Всеволод",
    202377873: "Тимофей",
    138716736: "Илья",
    306787585: "Мария",
    202038842: "Олег",
    352418484: "Михаил",
    142470714: "Захар",
    203626707: "Юрий",
    218147810: "Артем",
    253647021: "Павел",
    210835290: "Никита",
    175952275: "Иван",
    206038535: "Арсений",
    178728261: "Лада"
}

with open(GRAPH_FILENAME, "r") as file:
    data = yaml.safe_load(file)

G = nx.DiGraph() if data.get('directed', False) else nx.Graph()

for node in data['nodes']:
    G.add_node(node['id'])

for link in data['links']:
    G.add_edge(link['source'], link['target'])

plt.figure(figsize=(16, 12))
pos = nx.kamada_kawai_layout(G)

labels = {node['id']: id_to_name.get(node['id'], str(node['id'])) for node in data['nodes'] if node['id'] in id_to_name}

nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue', alpha=0.7)
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='black', font_weight='bold')

plt.title("Друзья друзей членов группы")
plt.savefig("friends-of-friends-of-colleagues.png")

plt.show()
