import vk_api
import networkx as nx
import yaml
import time
from dotenv import load_dotenv
import os

load_dotenv()

VK_TOKEN = os.getenv('VK_TOKEN')
VK_IDS = [
    225790978, 752279211
]

GRAPH_FILENAME = 'fofoc-true.yaml'
CACHE = {}


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

    friends = response['items']
    fr_in_lst = False

    for fr_id in friends:
        graph.add_edge(id, fr_id)
        if fr_id in VK_IDS:
            fr_in_lst = True

    if deep < 3:
        for fr_id in friends:
            fill_graph(vk, graph, fr_id, deep + 1, visited)

    if deep == 2:  # Работаем с друзьями друзей на глубине 2
        for i in range(len(friends)):
            for j in range(i + 1, len(friends)):
                friend_1 = friends[i]
                friend_2 = friends[j]
                graph.add_edge(friend_1, friend_2)

        for friend in friends:
            for vk_id in VK_IDS:
                if friend != vk_id:
                    if (friend, vk_id) in CACHE:
                        if CACHE[(friend, vk_id)]:
                            graph.add_edge(friend, vk_id)
                    else:
                        try:
                            mutual_friends = vk.friends.areFriends(user_ids=[friend, vk_id])
                            is_friend = mutual_friends[0]['friend_status'] == 3
                            CACHE[(friend, vk_id)] = is_friend
                            if is_friend:
                                graph.add_edge(friend, vk_id)
                        except vk_api.exceptions.ApiError as e:
                            print(f"VK api error on friend check {friend} and {vk_id}: {e}")

                    time.sleep(0.3)

def filter_graph(graph):
    nodes_to_remove = [node for node in graph.nodes if graph.degree(node) <= 1 and node not in VK_IDS]
    graph.remove_nodes_from(nodes_to_remove)

    to_remove_at_depth_4 = []
    for node in graph.nodes:
        if graph.degree(node) == 1:
            neighbor = list(graph.neighbors(node))[0]
            if graph.degree(neighbor) == 1 and neighbor not in VK_IDS:
                to_remove_at_depth_4.append(node)

    graph.remove_nodes_from(to_remove_at_depth_4)

def main():
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    friends_graph = nx.Graph()
    for id in VK_IDS:
        fill_graph(vk, friends_graph, id)

    filter_graph(friends_graph)

    print(f"Number of nodes after filtering: {friends_graph.number_of_nodes()}")

    with open(GRAPH_FILENAME, 'w') as file:
        yaml.dump(nx.node_link_data(friends_graph), file)

if __name__ == "__main__":
    main()
