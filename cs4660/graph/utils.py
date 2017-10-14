"""
utils package is for some quick utility methods

such as parsing
"""
from graph.graph import Node
from graph.graph import Edge
#from graph import AdjacencyList

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __lt__(self, other):
        return self.x < other.x or self.y < other.y
    def __gt__(self, other):
        return self.x > other.x and self.y > other.y
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph
    string_data = []
    grid_data = []
    with open(file_path) as f:
        for line in f:
            string_data[:-1] = line
            #print("STRING 1: ", string_data)
            grid_data.append(string_data[::])
            #print("LINE 1: ", grid_data)

    #print("LINE 1: ", grid_data)
    del grid_data[0]
    del grid_data[-1]
    for x in range(len(grid_data)):
        del grid_data[x][0]
        del grid_data[x][-1]
        del grid_data[x][-1]
        del grid_data[x][-1]
    #print("LINE 1: ", grid_data)
    grid_y_counter = 0
    
    tile_symbol_holder = {}
    while grid_y_counter < len(grid_data):
        grid_x_counter = 0
        tile_x_counter = 0
        while grid_x_counter < len(grid_data[grid_y_counter]):
            #print(grid_data[grid_y_counter])
            pair_a = grid_data[grid_y_counter][grid_x_counter]
            pair_b = grid_data[grid_y_counter][grid_x_counter+1]
            if pair_a == '#':
                grid_x_counter += 2
                tile_x_counter += 1
            else:
                symbol = str(pair_a) + str(pair_b)
                tile = Tile(tile_x_counter, grid_y_counter, symbol)
                node = Node(tile)
                tile_symbol_holder.update({str(tile.x)+str(tile.y): tile.symbol})
                grid_x_counter += 2
                tile_x_counter += 1
                graph.add_node(node)
                #print("NODE: ", node)
                #print("SYMBOLS\n: ", tile_symbol_holder)
        grid_y_counter += 1

    for node in graph.list_of_nodes():
        if str(node.data.x-1)+str(node.data.y) in tile_symbol_holder.keys():
            tile_symbol = tile_symbol_holder[str(node.data.x-1)+str(node.data.y)]
            if Node(Tile(node.data.x-1, node.data.y, tile_symbol)) in graph.list_of_nodes():
                edge = Edge(node, Node(Tile(node.data.x-1, node.data.y, tile_symbol)), 1)
                graph.add_edge(edge)
                #print(edge)

        if str(node.data.x+1)+str(node.data.y) in tile_symbol_holder.keys():
            tile_symbol = tile_symbol_holder[str(node.data.x+1)+str(node.data.y)]
            if Node(Tile(node.data.x+1, node.data.y, tile_symbol)) in graph.list_of_nodes():
                edge = Edge(node, Node(Tile(node.data.x+1, node.data.y, tile_symbol)), 1)
                graph.add_edge(edge)
                #print(edge)

        if str(node.data.x)+str(node.data.y-1) in tile_symbol_holder.keys():
            tile_symbol = tile_symbol_holder[str(node.data.x)+str(node.data.y-1)]
            if Node(Tile(node.data.x, node.data.y-1, tile_symbol)) in graph.list_of_nodes():
                edge = Edge(node, Node(Tile(node.data.x, node.data.y-1, tile_symbol)), 1)
                graph.add_edge(edge)
                #print(edge)

        if str(node.data.x)+str(node.data.y+1) in tile_symbol_holder.keys():
            tile_symbol = tile_symbol_holder[str(node.data.x)+str(node.data.y+1)]
            if Node(Tile(node.data.x, node.data.y+1, tile_symbol)) in graph.list_of_nodes():
                edge = Edge(node, Node(Tile(node.data.x, node.data.y+1, tile_symbol)), 1)
                graph.add_edge(edge)
                #print(edge)
    
    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    actions = ""
    for edge in edges:
        x_axis = edge.to_node.data.x - edge.from_node.data.x
        y_axis = edge.to_node.data.y - edge.from_node.data.y
        if x_axis > 0:
            actions += 'E'
        if x_axis < 0:
            actions += 'W'
        if y_axis > 0:
            actions += 'S'
        if y_axis < 0:
            actions += 'N'
    print(actions)       
    return actions

#parse_grid_file(AdjacencyList(), '../test/fixtures/grid-1.txt')