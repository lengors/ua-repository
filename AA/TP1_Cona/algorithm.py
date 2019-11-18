from graph import Graph
import time, itertools

# tests if a given set of colors associated to vertices produces a valid arrangment
def is_chromatic(vertices_colors, graph : Graph):
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor != vertex and vertices_colors[vertex] == vertices_colors[neighbor]:
                return False
    return True

def chromatic_number(graph : Graph):
    vertices, number = graph.vertices, None
    for color_set in itertools.product(range(len(vertices)), repeat = len(vertices)):
        chromatic_number = len(set(color_set))
        if (number is None or chromatic_number < number) and is_chromatic(dict(zip(vertices, color_set)), graph):
            number, comb = chromatic_number, list(zip(vertices, color_set))
    return number, comb

def timeit(executable, *args, **kwargs):
    start = time.time()
    result = executable(*args, **kwargs)
    return time.time() - start, result



''' 
Número cromático de um dado grafo não orientado G com n vértices e m arestas
Expressa o nº minimo de cores necessárias para colorir os vertices de G, de tal modo que a vértices adjacentes correspondam cores distintas.
'''


    