import matplotlib.pyplot as plt
import time, itertools, math
from graph import Graph

# tests if a given set of colors associated to vertices produces a valid arrangment
def is_chromatic(vertices_colors, graph : Graph):
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor != vertex and vertices_colors[vertex] == vertices_colors[neighbor]:
                    return False
    return True

def is_chromatic_configs(vertices_colors, graph : Graph):
    operations = 0
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor != vertex:
                operations += 1
                if vertices_colors[vertex] == vertices_colors[neighbor]:
                    return False, operations
    return True, operations

def chromatic_number(graph : Graph):
    vertices = graph.vertices
    for color_set in sorted(itertools.product(range(len(vertices)), repeat = len(vertices)), key = lambda colors : len(set(colors))):
        if is_chromatic(dict(zip(vertices, color_set)), graph):
            return len(set(color_set))
    return None

def chromatic_number_configs(graph : Graph):
    vertices = graph.vertices
    configs, operations = {}, 0
    for color_set in sorted(itertools.product(range(len(vertices)), repeat = len(vertices)), key = lambda colors : len(set(colors))):
        chromatic_number = len(set(color_set))
        is_true, ops = is_chromatic_configs(dict(zip(vertices, color_set)), graph)
        operations += ops
        configs[chromatic_number] = configs.get(chromatic_number, 0) + 1
        if is_true:
            return len(set(color_set)), operations, configs
    return None, operations, configs

def timeit(executable, *args, **kwargs):
    start = time.time()
    result = executable(*args, **kwargs)
    return time.time() - start, result

def main():
    amount = 10
    results = []
    intervals = 4
    min_vertices = 1
    max_vertices = 8
    print('Processing...')
    header = '(N. vertices, N. edges) - basic operations : average time : total tested solutions (N. different colors - tested solutions, ...)'
    with open('results.txt', 'w') as fin:
        fin.write('{}\n'.format(header))
    print(header)
    for vertices in range(min_vertices, max_vertices + 1): # [1, 20]
        max_edges = (vertices * (vertices - 1)) >> 1
        for index, edges in enumerate(sorted(set([ math.floor(max_edges * i / intervals) for i in range(1, intervals + 1) ]))):
            graph = Graph.random(directioned = False, allow_self = False, vertices = vertices, edges = edges)
            _, operations, configs = chromatic_number_configs(graph)
            average_time = sum([ timeit(chromatic_number, graph)[0] for j in range(amount) ]) / amount
            toprint = '({:02}, {:03}) - {} : {:06f} : {} ({})'.format(vertices, edges, operations, average_time, sum(configs.values()), ', '.join([
                    '{} - {}'.format(chromatic_number, count) for chromatic_number, count in sorted(configs.items(), key = lambda item : item[0]) ]))
            with open('results.txt', 'a') as fout:
                fout.write('{}\n'.format(toprint))
            print(toprint)
            if index == intervals - 1:
                results.append((vertices, average_time, operations))

    n_vertices, time_spent, n_operations = zip(*results)
    n_vertices, time_spent, n_operations = list(n_vertices), list(time_spent), list(n_operations)

    plt.plot(n_vertices, n_operations)
    plt.xlabel('N. of vertices')
    plt.ylabel('N. of operations')

    plt.figure()
    plt.plot(n_vertices, time_spent)
    plt.xlabel('N. of vertices')
    plt.ylabel('Time spent')

    plt.show()

if __name__ == '__main__':
    main()

''' 
Número cromático de um dado grafo não orientado G com n vértices e m arestas
Expressa o nº minimo de cores necessárias para colorir os vertices de G, de tal modo que a vértices adjacentes correspondam cores distintas.
'''


    