from gen_graph import generate_graph


def compute(graph):
    colors = [1]
    colors_graph = {num : 0 for num in range(len(graph))}
    colors_graph[0] = colors[0] # initialize algorithm
    for num, node in enumerate(graph[1:]):
        num_node = num + 1
        impossible_colors = list()
        add_color = True
        for num_sec_node, sec_node in enumerate(node):
            if num_sec_node != num_node and colors_graph[num_sec_node] != 0 and sec_node == 1:
                impossible_colors.append(colors_graph[num_sec_node])
        
        for color in colors:
            if not color in impossible_colors:
                colors_graph[num_node] = color
                add_color = False
        
        if add_color:
            new_color = colors[-1] + 1
            colors.append(new_color)
            colors_graph[num_node] = new_color
        

        

    return len(colors)




if __name__ == "__main__":
    graph = [
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        
    ]


    num_colors = compute(graph)
    print(num_colors)


''' 
Número cromático de um dado grafo não orientado G com n vértices e m arestas
Expressa o nº minimo de cores necessárias para colorir os vertices de G, de tal modo que a vértices adjacentes correspondam cores distintas.
'''


    