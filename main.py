import argparse
import copy
import time
from itertools import combinations

def log_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"The Algorithm {func.__name__} took {execution_time:.5f} seconds to execute.")

        return result
    return wrapper

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

    @log_time
    def high_degree_heuristic(self):
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
    
    @log_time
    def brute_force_vertex_cover(self):
        vertices = list(range(self.vertices))
        min_vertex_cover = None
        min_size = float('inf')

        total_combinations = sum(1 for k in range(1, self.vertices + 1) for _ in combinations(vertices, k))
        current_combination = 0
        last_printed_percentage = -1

        for k in range(1, self.vertices + 1):
            for subset in combinations(vertices, k):
                current_combination += 1
                progress_percentage = (current_combination / total_combinations) * 100
                if progress_percentage >= last_printed_percentage + 6:
                    last_printed_percentage = progress_percentage
                    print(f"Progress: {progress_percentage:.1f}%")

                temp_graph = self.copy_graph()
                is_vertex_cover = True

                for v in subset:
                    if not temp_graph.list[v]:
                        is_vertex_cover = False
                        break

                    temp = temp_graph.list[v].copy()
                    for neighbor in temp:
                        temp_graph.remove_edge(v, neighbor)

                if is_vertex_cover and temp_graph.is_empty():
                    if len(subset) < min_size:
                        min_size = len(subset)
                        min_vertex_cover = set(subset)

        print()
        return list(min_vertex_cover)

    def copy_graph(self):
        new_graph = Graph(self.vertices)
        new_graph.list = {v: neighbors.copy() for v, neighbors in self.list.items()}
        return new_graph

    def is_empty(self):
        return all(not neighbors for neighbors in self.list.values())

def main():
    parser = argparse.ArgumentParser("Trabalho Grafos")
    parser.add_argument("input_file", help="the path for the input file. Ex: input.txt", type=str)
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        n_vertex = int(f.readline().strip())
        n_edges = int(f.readline().strip())

        heuristic_graph = Graph(n_vertex)

        for _ in range(n_edges):
            u, v = map(int, f.readline().strip().split())
            heuristic_graph.add_edge(u, v)

        brute_force_graph = copy.deepcopy(heuristic_graph)

        print("Starting minimum vertex coverage using the highest degree heuristic...\n")
        list_of_vertex = heuristic_graph.high_degree_heuristic()
        print(f"Minimum vertex cover: {list_of_vertex}")
        print(f"Number of vertex used: {len(list_of_vertex)}\n")

        print("============================================================================\n")

        print("Starting minimum vertex coverage using the brute force algorithm...\n")
        list_of_vertex = brute_force_graph.brute_force_vertex_cover()
        print(f"Minimum vertex cover: {list_of_vertex}")
        print(f"Number of vertex used: {len(list_of_vertex)}")

if __name__ == '__main__':
    main()
