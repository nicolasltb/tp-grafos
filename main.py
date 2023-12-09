import argparse

class Graph:

    def __init__(self, vertices: int):
        self.vertices = vertices
        self.list = {i: [] for i in range(vertices)}

    def add_edge(self, u: int, v: int):
        self.list[u].append(v)
        self.list[v].append(u)

    def remove_edge(self, u: int, v: int):
        self.list[u].remove(v)
        self.list[v].remove(u)

    def get_degrees(self):
        return {v: len(neighbors) for v, neighbors in self.list.items()}

    def sprinklizacao(self):
        degrees = self.get_degrees()

        sorted_vertex = sorted(degrees.keys(), key=lambda v: degrees[v], reverse=True)

        vertex_cover = set()

        vertex = sorted_vertex[0]
        while len(self.list[vertex]):
            if vertex not in vertex_cover:
                vertex_cover.add(vertex)

                temp = self.list[vertex].copy()
                for v in temp:
                    self.remove_edge(vertex, v)

                degrees = self.get_degrees()
                sorted_vertex = sorted(degrees.keys(), key=lambda v: degrees[v], reverse=True)
                if sorted_vertex:
                    vertex = sorted_vertex[0]

        return list(vertex_cover)


def main():
    parser = argparse.ArgumentParser("Trabalho Grafos")
    parser.add_argument("input_file", help="the path for the input file. Ex: input.txt", type=str)
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        n_vertex = int(f.readline().strip())
        n_edges = int(f.readline().strip())

        graph = Graph(n_vertex)

        for i in range(n_edges):
            u, v = map(int, f.readline().strip().split())
            graph.add_edge(u, v)

        print(graph.sprinklizacao())

if __name__ == '__main__':
    main()
