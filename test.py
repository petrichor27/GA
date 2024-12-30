import random


def create_population(num_individuals, num_vertices):
    population = []
    for _ in range(num_individuals):
        individual = [random.randint(0, 1) for _ in range(num_vertices)]
        population.append(individual)
    return population


def fitness_function(individual, graph):
    # Реализуйте функцию для вычисления пригодности особи
    pass


def genetic_algorithm(graph, num_individuals, num_generations):
    # Создаем начальную популяцию
    population = create_population(num_individuals, len(graph))

    for _ in range(num_generations):
        # Оцениваем пригодность каждой особи
        fitness_scores = [fitness_function(individual, graph) for individual in population]

        # Выбираем лучшие особи для кроссовера
        selected_individuals = [population[i] for i in
                                sorted(range(len(population)), key=lambda x: fitness_scores[x], reverse=True)[
                                :num_individuals // 2]]

        # Кроссовер
        for _ in range(num_individuals - len(selected_individuals)):
            parent1, parent2 = random.sample(selected_individuals, 2)
            split_point = random.randint(1, len(parent1) - 1)
            child = parent1[:split_point] + parent2[split_point:]
            population.append(child)

        # Мутация
        for i in range(num_individuals):
            if random.random() < 0.1:  # Вероятность мутации 0.1
                mutation_point = random.randint(0, len(population[i]) - 1)
                population[i][mutation_point] = 1 - population[i][mutation_point]

    best_individual = max(population, key=lambda x: fitness_function(x, graph))
    return best_individual


# Пример графа
graph = [(1, 2), (2, 3), (3, 4), (4, 5)]
num_individuals = int(input("Введите количество особей: "))
num_vertices = len(graph)
num_generations = int(input("Введите количество поколений: "))

best_solution = genetic_algorithm(graph, num_individuals, num_generations)
print("Лучшая особь:", best_solution)
