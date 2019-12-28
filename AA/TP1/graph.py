import random, sys, math

class Graph:
    @staticmethod
    def __generate_possibilities_0(vertices):
        return [ (vertex0, vertex1) for vertex0 in vertices for vertex1 in vertices ]

    @staticmethod
    def __generate_possibilities_1(vertices):
        return [ (vertex0, vertex1) for vertex0 in vertices for vertex1 in vertices if vertex0 != vertex1 ]

    @staticmethod
    def __generate_possibilities_2(vertices):
        return [ (vertices[i], vertices[j]) for i in range(len(vertices)) for j in range(i, len(vertices)) ]

    @staticmethod
    def __generate_possibilities_3(vertices):
        return [ (vertices[i], vertices[j]) for i in range(len(vertices)) for j in range(i + 1, len(vertices)) ]

    __EQUATIONS = {
        (True, True) : (lambda x: x * x, lambda x: math.floor(math.sqrt(x)), __generate_possibilities_0),
        (True, False) : (lambda x: x * (x - 1), lambda x: math.floor((1 + math.sqrt(1 + (x << 2))) / 2), __generate_possibilities_1),
        (False, True) : (lambda x: (x * (x + 1)) >> 1, lambda x: math.floor((math.sqrt(1 + (x << 3)) - 1) / 2), __generate_possibilities_2),
        (False, False) : (lambda x: (x * (x - 1)) >> 1, lambda x: math.floor((math.sqrt(1 + (x << 3)) + 1) / 2), __generate_possibilities_3)
    }

    def __init__(self, directioned : bool, graph_data : dict = None):
        self.graph_data = dict() if graph_data is None else graph_data 
        self.add_edge = self.__add_edge_1 if directioned else self.__add_edge_0

    def __add_edge_0(self, node, neighbor):
        self.graph_data.setdefault(node, []).append(neighbor)
        if node != neighbor:
            self.graph_data.setdefault(neighbor, []).append(node)

    def __add_edge_1(self, node, neighbor):
        self.graph_data.setdefault(node, []).append(neighbor)

    def add_node(self, node):
        self.graph_data.setdefault(node, [])
    
    def __getitem__(self, vertex):
        return self.graph_data[vertex]

    def items(self):
        return self.graph_data.items()

    @property
    def edges(self):
        edges = set()
        for vertex, neighbors in self.graph_data.items():
            for neighbor in neighbors:
                v0, v1 = (vertex, neighbor), (neighbor, vertex)
                if v0 not in edges and v1 not in edges:
                    edges.add(v0)
        return list(edges)

    @property
    def edges_count(self):
        return sum([ len(neighbors) for neighbors in self.graph_data.values() ])

    @property
    def is_directioned(self):
        return self.add_edge == self.__add_edge_1

    @property
    def vertices(self):
        return list(self.graph_data.keys())

    @property
    def vertices_count(self):
        return len(self.graph_data)

    @staticmethod
    def random(directioned = None, allow_self = None, vertices = None, edges = None, max_vertices = None, max_edges = None):
        # Get graph type
        if directioned is None:
            directioned = bool(random.randint(0, 1))
        if allow_self is None:
            allow_self = bool(random.randint(0, 1))
        
        # Get graph type equations
        max_edges_equation, max_vertices_equation, generate_possibilites = Graph.__EQUATIONS[(directioned, allow_self)]
        
        # Get number of vertices and edges of graph
        if vertices is None:
            if max_vertices is None:
                max_vertices = max_vertices_equation(sys.maxsize)
            vertices = random.randint(1, max_vertices)
        if edges is None:
            max_edges = max_edges_equation(vertices) if max_edges is None else max(max_edges, max_edges_equation(vertices))
            edges = random.randint(0, max_edges)
        edges = min(edges, max_edges_equation(vertices))

        # Generate graph based on those numbers
        vertices = list(range(vertices))

        # Possibilities
        graph_possibilities = generate_possibilites.__func__(vertices)

        # Create graph
        graph = Graph(directioned)

        # Generate random graph
        for _ in range(edges):
            index = random.randint(0, len(graph_possibilities) - 1)
            graph.add_edge(*graph_possibilities.pop(index))

        # Ensures all vertices exist on graph
        for vertex in vertices:
            graph.add_node(vertex)

        return graph