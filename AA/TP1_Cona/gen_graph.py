import sys
from random import randint


def generate_graph(v):
    graph = list(list(-1 for _ in range(v)) for _ in range(v))
    for node, sub_list in enumerate(graph):
        for i, inter in enumerate(sub_list):
            if inter == -1:
                line = randint(0, 1)
                sub_list[i] = line
                graph[i][node] = line

    return graph



def print_graph(graph):
    for l in graph:
        print(l)





if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Número de argumentos inválido!!")
        sys.exit(1)
    
    vertices = int(sys.argv[1]) if sys.argv[1].isdigit() else 0

    graph = generate_graph(vertices)
    print_graph(graph)
