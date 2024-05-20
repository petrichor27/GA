import random
import networkx as nx


class GADarwin:
    # Генерация начальной популяции, все в истоке стоят
    def __init__(self, nx_graph, graph_size: int, population_size: int, iterations: int, mutation_probability: float):
        self.graph_size = graph_size
        self.graph = nx_graph
        self.population_size = population_size
        self.iterations = iterations
        self.mutation_probability = mutation_probability
        self.source = 0  # вершина исток
        self.sink = self.graph_size - 1  # вершина сток

    def generate_population(self) -> list[list[int]]:
        population = []
        for _ in range(self.population_size):
            # Генерация случайного пути от истока к стоку (в хромосоме особи сохранен этот путь)
            path = [self.source]
            while path[-1] != self.sink:
                neighbors = list(self.graph.successors(path[-1]))
                if not neighbors:
                    break
                next_node = random.choice(neighbors)
                path.append(next_node)
            population.append(path)
        return population

    def fitness(self, individual: list[int]) -> int:
        path_with_weights = []
        for i in range(len(individual) - 1):
            path_with_weights.append(self.graph.get_edge_data(individual[i], individual[i + 1])['weight'])
        return min(path_with_weights)

    # Оператор селекции (рулеточное колесо)
    def selection(self, population: list[list[int]], fitness_values: list[int]) -> list[int]:
        total_fitness = sum(fitness_values)
        probabilities = [fitness / total_fitness for fitness in fitness_values]
        rand = random.uniform(0, total_fitness)
        cumulative_probability = 0
        while True:
            for i, prob in enumerate(probabilities):
                cumulative_probability += prob
                if cumulative_probability > rand:
                    return population[i]

    # def catastrophe(self, population: list[list[int]]):
    #     dead = random.randint(int(len(population) * 0.1), len(population))
    #     return population[:-dead]

    # Скрещивание (пути объединяются в какой-то точке)
    def crossover(self, parent1: list[int], parent2: list[int]) -> list[list[int]]:
        common = set(parent1[1:-2]) & set(parent2[1:-2])
        if not common:
            return random.choice([parent1, parent2])

        count_of_children = random.randint(1, 3)
        children = []
        for _ in range(count_of_children):
            child = []
            crossover_point = random.choice([i for i in common])
            first_p = random.choice([parent1, parent2])
            second_p = parent1 if first_p == parent2 else parent2
            for i in first_p:
                if i != crossover_point:
                    child.append(i)
                else:
                    break
            i = 0
            while i < len(second_p):
                if second_p[i] != crossover_point:
                    i += 1
                else:
                    break
            while i < len(second_p):
                child.append(second_p[i])
                i += 1
            children.append(child)
        return children

    # Оператор мутации (одна вершина меняется и путь дальше перестраивается)
    def mutation(self, individual: list[int]):
        temp = individual.copy()
        print("До мутации: ", individual)
        mutate_index = random.randint(1, len(individual) - 2)
        previous_node = individual[mutate_index - 1]
        individual = individual[:mutate_index]
        new_node = -1
        while new_node != self.sink:
            neighbors = list(self.graph.successors(previous_node))
            new_node = random.choice(neighbors)
            if new_node not in individual:
                individual.append(new_node)
                previous_node = individual[-1]
                mutate_index += 1
            elif all(elem in individual for elem in neighbors):
                print("Мутация невозможна")
                individual = temp
                break
        print("После мутации: ", individual)
        print("---------------")
        return individual

    def genetic_algorithm(self) -> tuple[int, list[int]]:
        population = self.generate_population()

        for _ in range(self.iterations):
            fitness_values = [self.fitness(individual) for individual in population]
            new_population = []
            for _ in range(self.population_size):
                parent1 = self.selection(population, fitness_values)
                parent2 = self.selection(population, fitness_values)
                children = self.crossover(parent1, parent2)
                for child in children:
                    if random.uniform(0, 1) < self.mutation_probability and len(child) > 2:
                        child = self.mutation(child)
                    new_population.append(child)
            population = sorted(new_population, key=lambda ind: self.fitness(ind), reverse=True)[:self.population_size]

        best_individual = max(population, key=lambda ind: self.fitness(ind))
        max_flow = self.fitness(best_individual)
        return max_flow, best_individual
