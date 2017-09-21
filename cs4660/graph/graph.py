"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns True if node_1 and node_2 are directly connected or False otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns True if the node is added and False if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns True if the node is removed and False if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns True if the edge is added and False if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns True if the edge is removed and False if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    import re
    with open(file_path) as f:
        first_line = int(f.readline().rstrip())
        x = 0
        while x < first_line:
            graph.add_node(Node(x))
            x += 1

        for line in f:
            string_data = re.split('[:\n]', line)
            del string_data[-1]
            int_data = [int(x) for x in string_data]
            graph.add_edge(Edge(Node(int_data[0]), Node(int_data[1]), int_data[2]))

    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        list_of_edges =  self.adjacency_list[node_1]
        for edge in list_of_edges:
            if node_2 == edge.to_node:
                return True
        return False

    def neighbors(self, node):
        edges_list = self.adjacency_list[node]
        neighbors_list = []
        for edge in edges_list:
            neighbors_list.append(edge.to_node)

        return neighbors_list

    def add_node(self, node):
        if node in self.adjacency_list.keys():
            return False
        else:
            self.adjacency_list.update({node: []})
            return True

    def remove_node(self, node):
        if node in self.adjacency_list.keys():
            neighbor = list(self.adjacency_list.keys())
            x = 0
            while x < len(neighbor):
                neighbors_list = self.neighbors(neighbor[x])
                for temp_node in neighbors_list:
                    if temp_node == node:
                        edges = self.adjacency_list[neighbor[x]]
                        for edge in edges:
                            if edge.to_node == node:
                                self.adjacency_list[neighbor[x]].remove(edge)
                x += 1                
                        
            del self.adjacency_list[node]
            return True
        else:
            return False

    def add_edge(self, edge):
        if self.adjacent(edge.from_node, edge.to_node):
            return False
        else:
            self.adjacency_list[edge.from_node].append(edge)
            return True

    def remove_edge(self, edge):
        if self.adjacent(edge.from_node, edge.to_node):
            self.adjacency_list[edge.from_node].remove(edge)
            return True
        else:
            return False

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        return self.adjacency_matrix[node_1.data][node_2.data] > 0

    def neighbors(self, node):
        list_of_neighbors = self.adjacency_matrix[node.data]
        neighbors_list = []
        x = 0
        while x < len(list_of_neighbors):
            if list_of_neighbors[x] > 0:
                neighbors_list.append(Node(x))
            x += 1
        return neighbors_list


    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node)
            self.adjacency_matrix = [[0 for x in range(len(self.nodes))] for x in range(len(self.nodes))]
            return True

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes = [x for x in self.nodes if x != node]
            self.adjacency_matrix[node.data] = [0 for x in range(len(self.nodes))]
            counter = 0
            for x in self.adjacency_matrix:
                self.remove_edge(Edge(Node(counter), node, x[node.data]))
                counter += 1
            
            return True
        else:
            return False

    def add_edge(self, edge):
        if edge.weight == self.adjacency_matrix[edge.from_node.data][edge.to_node.data]:
            return False
        else:
            self.adjacency_matrix[edge.from_node.data][edge.to_node.data] = edge.weight
            return True

    def remove_edge(self, edge):
        if edge.weight == self.adjacency_matrix[edge.from_node.data][edge.to_node.data]:
            self.adjacency_matrix[edge.from_node.data][edge.to_node.data] = 0
            return True
        else:
            return False

    def __get_node_index(self, node):
        """helper method to find node index"""
        if node in self.nodes:
            return self.nodes.index(node)
        else:
            return -1


class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if edge.from_node == node_1 and edge.to_node == node_2:
                return True

        return False

    def neighbors(self, node):
        neighbors_list = []
        for edge in self.edges:
            if edge.from_node == node:
                neighbors_list.append(edge.to_node)

        return neighbors_list

    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node)
            return True

    def remove_node(self, node):
        if node in self.nodes:
            del self.nodes[self.nodes.index(node)]
            for edge in self.edges:
                if edge.to_node == node:
                    self.remove_edge(edge)
            return True
        else:
            return False

    def add_edge(self, edge):
        if edge in self.edges:
            return False
        else:
            self.edges.append(edge)
            return True 

    def remove_edge(self, edge):
        if edge in self.edges:
            del self.edges[self.edges.index(edge)]
            return True
        else:
            return False 

