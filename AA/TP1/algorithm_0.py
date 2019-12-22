from graph import Graph
import time, itertools

def is_chromatic_0(vertices_colors, graph : Graph):
    for vertex, neighbors in graph.items():
        if any([ vertices_colors[vertex] == vertices_colors[neighbor] for neighbor in neighbors if neighbor != vertex ]):
            return False
    return True

def is_chromatic_1(vertices_colors, graph : Graph):
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            if neighbor != vertex and vertices_colors[vertex] == vertices_colors[neighbor]:
                return False
    return True

def chromatic_number_0(graph : Graph):
    counter = 0
    number = None
    toconitnue = True
    vertices = graph.vertices
    colors = [ 0 for _ in range(len(vertices)) ]

    while toconitnue:
        chromatic_number = len(set(colors)) # get different amount of colors
        if (number is None or chromatic_number < number) and is_chromatic_0(dict(zip(vertices, colors)), graph): # if no chromatic arrangment yet or the different
            number = chromatic_number # update smallest number
            comb = list(zip(vertices, colors))

        colors[counter] += 1
        if colors[counter] >= len(vertices):
            keep = True
            while keep:
                if counter == len(colors) - 1:
                    return number, comb
                colors[counter] = 0
                counter += 1
                colors[counter] += 1
                keep = colors[counter] >= len(vertices)
            counter = 0

def chromatic_number_1(graph : Graph):
    counter = 0
    number = None
    toconitnue = True
    vertices = graph.vertices
    colors = [ 0 for _ in range(len(vertices)) ]

    while toconitnue:
        chromatic_number = len(set(colors)) # get different amount of colors
        if (number is None or chromatic_number < number) and is_chromatic_1(dict(zip(vertices, colors)), graph): # if no chromatic arrangment yet or the different
            number = chromatic_number # update smallest number
            comb = list(zip(vertices, colors))

        colors[counter] += 1
        if colors[counter] >= len(vertices):
            keep = True
            while keep:
                if counter == len(colors) - 1:
                    return number, comb
                colors[counter] = 0
                counter += 1
                colors[counter] += 1
                keep = colors[counter] >= len(vertices)
            counter = 0

def chromatic_number_2(graph : Graph):
    counter = 0
    number = None
    toconitnue = True
    vertices = graph.vertices
    colors = [ 0 for _ in range(len(vertices)) ]

    while toconitnue:
        chromatic_number = len(set(colors)) # get different amount of colors
        vertices_colors = dict(zip(vertices, colors))
        if (number is None or chromatic_number < number) and all([ all([ colors[vertex] != colors[neighbor] for neighbor in neighbors if neighbor != vertex ]) for vertex, neighbors in graph.items() ]): # if no chromatic arrangment yet or the different
            number = chromatic_number # update smallest number
            comb = list(zip(vertices, colors))

        colors[counter] += 1
        if colors[counter] >= len(vertices):
            keep = True
            while keep:
                if counter == len(colors) - 1:
                    return number, comb
                colors[counter] = 0
                counter += 1
                colors[counter] += 1
                keep = colors[counter] >= len(vertices)
            counter = 0

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
            number = chromatic_number
    return number

def timeit(executable, *args, **kwargs):
    start = time.time()
    result = executable(*args, **kwargs)
    return time.time() - start, result

total0 = 0
total1 = 0
total2 = 0
amount = 1000
results0 = list()
for i in range(amount):
    g = Graph.random(directioned = False, max_vertices = 6)
    t0, r = timeit(chromatic_number_0, g)
    t1, r = timeit(chromatic_number_1, g)
    t2, r = timeit(chromatic_number_2, g)
    total0 += t0
    total1 += t1
    total2 += t2

print(total0 / amount)
print(total1 / amount)
print(total2 / amount)

results1 = list()
for i in range(amount):
    g = Graph.random(directioned = True, max_vertices = 6)
    t0, r = timeit(chromatic_number_0, g)
    t1, r = timeit(chromatic_number_1, g)
    t2, r = timeit(chromatic_number_2, g)
    total0 += t0
    total1 += t1
    total2 += t2

print(total0 / (2 * amount))
print(total1 / (2 * amount))
print(total2 / (2 * amount))

''' 
Número cromático de um dado grafo não orientado G com n vértices e m arestas
Expressa o nº minimo de cores necessárias para colorir os vertices de G, de tal modo que a vértices adjacentes correspondam cores distintas.
'''


    