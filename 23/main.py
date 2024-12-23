import os
import networkx as nx

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_data():
    connections = []
    with open(filename) as f:
        for line in f.readlines():
            connections.append([x for x in line.strip().split("-")])
    return connections


def main_one():
    connections = get_data()
    
    G = nx.Graph()
    for connection in connections:
        node1, node2 = connection
        G.add_edge(node1, node2)
        
    def starts_with_t(triangle):
        return triangle[0].startswith("t") or\
                triangle[1].startswith("t") or\
                    triangle[2].startswith("t")

    triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
    return sum(1 if starts_with_t(triangle) else 0 for triangle in triangles)
    


def main_two():
    connections = get_data()
    
    G = nx.Graph()
    for connection in connections:
        node1, node2 = connection
        G.add_edge(node1, node2)
        
    cliques = list(nx.find_cliques(G))
    largest_clique = max(cliques, key=len)
    return ",".join(sorted(largest_clique))


if __name__ == "__main__":
    print(main_one())
    print(main_two())
