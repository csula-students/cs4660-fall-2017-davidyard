"""
Searches module defines all different search algorithms
"""
from graph.graph import Edge
from graph.graph import Node
from graph.utils import Tile
from queue import *


def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = Queue(maxsize=0)
    q.put(initial_node)
    actions = []
    node_path = []
    visited = [initial_node]
    parent_list = {} #set up so it is child: parent
    parent_list.update({initial_node: "No Parent"})
    distance_list = {}
    while not q.empty():
        node_from_q = q.get()
        parent_distance = 0
        distance_list.update({node_from_q: parent_distance})
        for node in graph.neighbors(node_from_q):
            if node not in visited:
                parent_list.update({node: node_from_q})
                parent_distance = graph.distance(node_from_q, node) + distance_list[node_from_q]
                distance_list.update({node: parent_distance})
                if node == dest_node:
                    node_path.append(node)
                    while not q.empty():
                        q.get()
                else:
                    q.put(node)
                    visited.append(node)
    for node in node_path:
        if str(parent_list[node]) == "No Parent":
            break
        else:
            node_path.append(parent_list[node])
            actions.append(Edge(parent_list[node], node, graph.distance(parent_list[node], node)))

    #print("THE PATH IS: ",list(reversed(actions)))
    return list(reversed(actions))

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = PriorityQueue(maxsize=0)
    q.put((1, initial_node.data, 0, initial_node, 'Parent Node'))
    actions = []
    nodes_in_q = []
    node_path = []
    visited = [initial_node]
    parent_list = {} #set up so it is child: parent
    parent_list.update({initial_node: "No Parent"})
    x = (graph.total_number_of_nodes()*graph.total_number_of_nodes())*10
    for node in graph.neighbors(initial_node):
        #y = x*graph.total_number_of_nodes()
        if node not in nodes_in_q:
            q.put((graph.neighbors(initial_node).index(node), x, node.data,  node, initial_node))
            nodes_in_q.append(node)
            x -= 1
    while not q.empty():
        q_data = q.get()
        node_from_q = q_data[3]
        for node in graph.neighbors(node_from_q):
            #if node not in nodes_in_q:
            q.put((graph.neighbors(node_from_q).index(node), x, node.data,  node, node_from_q))
            nodes_in_q.append(node)
            x -= 1
        if node_from_q not in visited:
            parent_list.update({node_from_q: q_data[4]})
            visited.append(node_from_q)
            if node_from_q == dest_node:
                node_path.append(node_from_q)
                while not q.empty():
                    q.get()

    for node in node_path:
        if str(parent_list[node]) == "No Parent":
            break
        else:
            node_path.append(parent_list[node])
            actions.append(Edge(parent_list[node], node, graph.distance(parent_list[node], node)))

    return list(reversed(actions))

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = PriorityQueue(maxsize=0)
    distance = 0
    q.put((distance, initial_node.data, initial_node))
    actions = []
    node_path = []
    node_path.append(dest_node)
    visited = [initial_node]
    parent_list = {} #set up so it is child: an dictionary of parent
    parent_list[initial_node] = {'No Parent': 'No Parent'}
    distance_list = {} #set up so it is an edge and the total distance
    while not q.empty():
        node_from_q = q.get()[2]
        for node in graph.neighbors(node_from_q):
            if node not in visited:
                if node in parent_list:
                    parent_list[node].update({node_from_q:node_from_q})
                else:
                    parent_list[node] = {node_from_q: node_from_q}
                if node_from_q == initial_node:
                    distance = graph.distance(node_from_q, node)
                else:
                    distance = graph.distance(node_from_q, node) + distance_list[(list(parent_list[node_from_q].values())[0], node_from_q)]
                
                distance_list.update({(node_from_q, node): distance})
                if node == dest_node:
                    continue
                else:
                    q.put((distance, node.data, node))
                    visited.append(node)
    for node in node_path:
        if 'No Parent' in parent_list[node]:
            break
        else:
            p_dict = parent_list[node]
            if len(p_dict) > 1:
                x = 1
                min_node = list(p_dict.values())[0]
                while x < len(p_dict):
                    temp_node = list(p_dict.values())[x]
                    if distance_list[(temp_node, node)] < distance_list[(min_node, node)]:
                        min_node = temp_node
                    x += 1
                #print("Min Node is: ", min_node)
                #print("EDGRE is: ",Edge(min_node, node, graph.distance(min_node, node)))
                node_path.append(min_node)
                actions.append(Edge(min_node, node, graph.distance(min_node, node)))
            else:
                node_path.append(list(p_dict.values())[0])
                actions.append(Edge(list(p_dict.values())[0], node, graph.distance(list(p_dict.values())[0], node)))
            

    #print("THE PATH IS: ",list(reversed(actions)))
    return list(reversed(actions))

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = PriorityQueue(maxsize=0)
    q.put(initial_node, 0)
    edges = []
    came_from = {}
    cost_so_far = {}
    came_from[initial_node] = 'No Parent'
    cost_so_far[initial_node] = 0
    print("REACHED HERE\n")
    while not q.empty():
        current = q.get()
        if current == dest_node:
            break
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.distance(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                x_axis = abs(dest_node.data.x - next.data.x)
                y_axis = abs(dest_node.data.y - next.data.y)
                heuristic = x_axis + y_axis
                priority = new_cost + heuristic
                q.put(next, priority)
                came_from[next] = current

    for to_node in came_from.keys():
        from_node = came_from[to_node]
        if str(from_node) == 'No Parent':
            continue
        else:
            edge = Edge(from_node, to_node, 1)
            #print(edge)
            edges.append(edge)

    return edges