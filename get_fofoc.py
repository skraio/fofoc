import vk_api
import networkx as nx
import yaml
from dotenv import load_dotenv
import os

load_dotenv()

VK_TOKEN = os.getenv('VK_TOKEN')
VK_IDS = [
    225790978, 752279211, 202377873, 138716736, 306787585, 202038842,
    352418484, 142470714, 203626707, 218147810, 253647021, 210835290,
    175952275, 206038535, 178728261
]

GRAPH_FILENAME = 'friends-of-friends-of-colleagues.yaml'


def fill_graph(vk, graph, id, deep=1, visited=None):
    if visited is None:
        visited = set()

    if id in visited:
        return

    visited.add(id)

    max_cnt = 30

    try:
        response = vk.friends.get(user_id=id, count=max_cnt)
    except vk_api.exceptions.ApiError as e:
        if e.code == 30:
            print(f"Profile {id} is private, skipping...")
        else:
            print(f"VK api error on id {id} and deep {deep}\n {e}")
        return

    fr_in_lst = False
    for fr_id in response['items']:
        graph.add_edge(id, fr_id)
        if fr_id in VK_IDS:
            fr_in_lst = True

    if not fr_in_lst and deep < 2:
        for fr_id in response['items']:
            fill_graph(vk, graph, fr_id, deep + 1, visited)


def main():
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    friends_graph = nx.Graph()
    for id in VK_IDS:
        print(id)
        fill_graph(vk, friends_graph, id)

    print(f"Number of nodes: {friends_graph.number_of_nodes()}")

    with open(GRAPH_FILENAME, 'w') as file:
        yaml.dump(nx.node_link_data(friends_graph), file)

if __name__ == "__main__":
    main()
