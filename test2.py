import random

# Граф представлен в виде матрицы смежности
graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

# Размер графа
graph_size = len(graph)

# Функция вычисления потока в графе
def calculate_flow(path):
    flow = float('inf')

    for i in range(graph_size - 1):
        try:
            flow = min(flow, graph[path[i]][path[i + 1]])
        except Exception as e:
            print(e)
            print(flow)
            print(i)
            print(path)
            print(path[i])
            print(path[i + 1])
            print(graph[path[i]][path[i + 1]])

    return flow

# Генерация начальной популяции случайных путей
def generate_population(population_size):
    population = []
    for _ in range(population_size):
        path = [0]
        while path[-1] != graph_size - 1:
            next_node = random.randint(1, graph_size - 1)
            path.append(next_node)
        population.append(path)
    return population

# Оператор селекции (рулеточное колесо)
def selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    rand = random.uniform(0, total_fitness)
    cumulative_probability = 0
    for i, path in enumerate(population):
        cumulative_probability += fitness_values[i]
        if cumulative_probability > rand:
            return path

# Оператор кроссовера (одноточечный)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

# Оператор мутации (перемещение одной вершины)
def mutation(path):
    mutate_index = random.randint(1, len(path) - 2)
    mutation_node = random.randint(1, graph_size - 2)
    path[mutate_index] = mutation_node
    return path

# Генетический алгоритм
def genetic_algorithm(population_size, generations):
    population = generate_population(population_size)
    for _ in range(generations):
        fitness_values = [calculate_flow(path) for path in population]  # scores = [nx.maximum_flow(graph, s, t)[0] for s, t in population]
        new_population = []
        for _ in range(population_size):
            parent1 = selection(population, fitness_values)
            parent2 = selection(population, fitness_values)
            child = crossover(parent1, parent2)
            if random.uniform(0, 1) < 0.1:  # Вероятность мутации
                child = mutation(child)
            new_population.append(child)
        population = new_population
    best_path = max(population, key=lambda path: calculate_flow(path))
    max_flow = calculate_flow(best_path)
    return best_path, max_flow

# Пример использования
population_size = 50
generations = 1000
best_path, max_flow = genetic_algorithm(population_size, generations)
print("Best Path:", best_path)
print("Max Flow:", max_flow)