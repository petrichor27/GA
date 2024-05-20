import random


def generate_random_digraph(n: int) -> list[tuple[int, int, int]]:
    edges = []
    graph = {i: set() for i in range(0, n)}

    for i in range(n):
        for j in range(n):
            if i != j and i not in graph[j] and random.random() < 0.3:
                v = random.randint(1, 10)
                edges.append((i, j, v))
                graph[i].add(j)

    # Make sure graph is connected
    for i in range(n - 1):
        if not graph[i]:
            j = i
            while j == i:
                j = random.randint(0, n - 1)
            graph[i].add(j)
            v = random.randint(1, 10)
            edges.append((i, j, v))

    return edges
