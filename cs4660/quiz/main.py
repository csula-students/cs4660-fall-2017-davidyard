"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
from queue import *

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def bfs(initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = Queue(maxsize=0)
    q.put(initial_node)
    actions = []
    node_path = []
    visited = [initial_node['id']]
    parent_list = {} #set up so it is child: parent
    parent_list.update({initial_node['id']: "No Parent"})
    distance_list = {}
    parent_distance = 0
    distance_list.update({initial_node['id']: parent_distance})
    while not q.empty():
        node_from_q = q.get()
        if len(node_from_q['neighbors']) < 1:
            node_from_q = get_state(node_from_q['id'])
        for node in node_from_q['neighbors']:
            if node['id'] not in visited:
                parent_list.update({node['id']: node_from_q})
                #print(parent_list)
                parent_distance = transition_state(empty_room['id'], empty_room['neighbors'][0]['id'])['event']['effect'] + distance_list[node_from_q['id']]
                distance_list.update({node['id']: parent_distance})
                
                if node['id'] == dest_node['id']:
                    #print("DESCUDH: ",dest_node['id'])
                    node_path.append(node)
                    while not q.empty():
                        q.get()
                else:
                    q.put(node)
                    visited.append(node['id'])
                    #print('\n',node)
                    #print('\n',q.empty())
    for node in node_path:
        if str(parent_list[node['id']]) == "No Parent":
            break
        else:
            node_path.append(parent_list[node['id']])
            from_node = parent_list[node['id']]['location']['name'] + " (" + parent_list[node['id']]['id']+") "
            to_node = node['location']['name'] + " (" + node['id']+") "
            weight = ": " + str(transition_state(parent_list[node['id']]['id'], node['id'])['event']['effect'])
            actions.append(from_node + to_node + weight)
            #print("tonode\n", to_node)

    return list(reversed(actions))

def dijkstra(initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = PriorityQueue(maxsize=0)
    q.put((0, initial_node['id'], initial_node))
    actions = []
    node_path = []
    node_path.append(dest_node)
    visited = [initial_node['id']]
    parent_list = {} #set up so it is child: parent
    parent_list[initial_node['id']] = {'No Parent': 'No Parent'}
    distance_list = {}
    parent_distance = 0
    hp = {}
    distance_list.update({initial_node['id']: parent_distance})
    while not q.empty():
        node_from_q = q.get()[2]
        if len(node_from_q['neighbors']) < 1:
            node_from_q = get_state(node_from_q['id'])
        for node in node_from_q['neighbors']:
            if node['id'] not in visited:
                if node['id'] in parent_list:
                    parent_list[node['id']].update({node_from_q['id']:node_from_q})
                    #print("HERE")
                else:
                    parent_list[node['id']] = {node_from_q['id']: node_from_q}
                    #print("BECKS")

                if node_from_q['id'] == initial_node['id']:
                    parent_distance = transition_state(node_from_q['id'], node['id'])['event']['effect']
                    hp[(node_from_q['id'], node['id'])] = parent_distance
                else:
                    #print(list(parent_list[node_from_q['id']].values())[0])
                    pounds = transition_state(node_from_q['id'], node['id'])['event']['effect']
                    hp[(node_from_q['id'], node['id'])] = pounds
                    parent_distance = pounds + distance_list[(list(parent_list[node_from_q['id']].keys())[0], node_from_q['id'])]
                
                distance_list.update({(node_from_q['id'], node['id']): parent_distance})
                
                if node['id'] == dest_node['id']:
                    continue
                else:
                    #print("priority: ",priority)
                    q.put((-parent_distance, node['id'], node))
                    visited.append(node['id'])
                    #print("ELDS|")
    for node in node_path:
        if str(list(parent_list[node['id']].values())[0]) == "No Parent":
            break
        else:
            #print("JSKFH", list(parent_list[node['id']].values())[0]['id'])
            node_path.append(list(parent_list[node['id']].values())[0])
            from_node = list(parent_list[node['id']].values())[0]['location']['name'] + " (" + list(parent_list[node['id']].values())[0]['id']+") "
            to_node = node['location']['name'] + " (" + node['id']+") "
            weight = ": " + str(hp[list(parent_list[node['id']].values())[0]['id'], node['id']])
            actions.append(from_node + to_node + weight)
            #print("tonode\n", to_node)
    #print(node_path)
    print("THE Total HP for Dijkstra is: ",distance_list[(list(parent_list['f1f131f647621a4be7c71292e79613f9'].keys())[0], 'f1f131f647621a4be7c71292e79613f9')])
    return list(reversed(actions))

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response


if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    end_room = get_state('f1f131f647621a4be7c71292e79613f9')
    #print(empty_room)
    #print("NEIFHJEBHFKJDHBFO\n", empty_room['neighbors'])
    #print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id'])) #['event']['effect'] is to get weight
    print("BFS\n",bfs(empty_room, end_room))
    print("DIJKSTRA\n",dijkstra(empty_room, end_room))
