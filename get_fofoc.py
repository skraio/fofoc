import vk_api
import yaml
import networkx as nx
from dotenv import load_dotenv
import os
import time

load_dotenv()

VK_TOKEN = os.getenv('VK_TOKEN')
VK_IDS = [
    202377873,
    210835290
]

GRAPH_FILENAME = 'fofoc.yaml'
PROGRESS_FILENAME = 'progress.yaml'


def save_graph(graph, filename):
    with open(filename, 'w') as file:
        yaml.dump(nx.node_link_data(graph), file)


def load_graph(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
            return nx.node_link_graph(data)
    return nx.Graph()


def save_progress(processed_ids):
    with open(PROGRESS_FILENAME, 'w') as file:
        yaml.dump(processed_ids, file)


def load_progress():
    if os.path.exists(PROGRESS_FILENAME):
        with open(PROGRESS_FILENAME, 'r') as file:
            return yaml.safe_load(file)
    return set()


def fill_graph(vk, graph, id, processed_ids, deep=1):
    if id in processed_ids:
        return
    max_cnt = 30

    try:
        response = vk.friends.get(user_id=id, count=max_cnt)
    except vk_api.exceptions.ApiError as e:
        print(f"VK api error on id {id} and deep {deep}\n {e}")
        if 'Rate limit reached' in str(e):
            print("Saving progress due to rate limit...")
            save_graph(graph, GRAPH_FILENAME)
            save_progress(processed_ids)
            time.sleep(60)
        return

    fr_in_lst = False
    for fr_id in response['items']:
        graph.add_edge(id, fr_id)
        if fr_id in VK_IDS:
            fr_in_lst = True
    processed_ids.add(id)
    save_progress(processed_ids)

    if (not fr_in_lst) and (deep < 4):
        deep += 1
        for fr_id in response['items']:
            fill_graph(vk, graph, fr_id, processed_ids, deep)


def filter_graph(graph):
    nodes_to_remove = [node for node in graph.nodes if graph.degree(node) <= 1 and node not in VK_IDS]
    graph.remove_nodes_from(nodes_to_remove)


def main():
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()

    friends_graph = load_graph(GRAPH_FILENAME)
    processed_ids = load_progress()

    for id in VK_IDS:
        print(id)
        fill_graph(vk, friends_graph, id, processed_ids)

    filter_graph(friends_graph)

    print(f"Number of nodes: {friends_graph.number_of_nodes()}")

    save_graph(friends_graph, GRAPH_FILENAME)


if __name__ == "__main__":
    main()
