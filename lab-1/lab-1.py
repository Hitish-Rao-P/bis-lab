import random

TARGET = "1010101010101010"
TARGET_LENGTH = len(TARGET)
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.7
NUM_GENERATIONS = 1000
TOURNAMENT_SIZE = 5

def create_individual():
    return ''.join(random.choice('01') for _ in range(TARGET_LENGTH))

def fitness(individual):
    return sum(1 for i, c in enumerate(individual) if c == TARGET[i])

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        crossover_point = random.randint(1, TARGET_LENGTH - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    return parent1, parent2

def mutate(individual):
    if random.random() < MUTATION_RATE:
        mutate_pos = random.randint(0, TARGET_LENGTH - 1)
        individual = list(individual)
        individual[mutate_pos] = '1' if individual[mutate_pos] == '0' else '0'
        return ''.join(individual)
    return individual

def tournament_selection(population):
    tournament = random.sample(population, TOURNAMENT_SIZE)
    tournament.sort(key=lambda x: fitness(x), reverse=True)
    return tournament[0]

def genetic_algorithm():
    population = [create_individual() for _ in range(POPULATION_SIZE)]

    for generation in range(NUM_GENERATIONS):
        population.sort(key=lambda x: fitness(x), reverse=True)
        print(f"Generation {generation} - Best Fitness: {fitness(population[0])} - Best Individual: {population[0]}")

        if fitness(population[0]) == TARGET_LENGTH:
            print("Target reached!")
            break

        next_generation = []
        # Keep the best individual (elitism)
        next_generation.append(population[0])

        while len(next_generation) < POPULATION_SIZE:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_generation.append(child1)
            if len(next_generation) < POPULATION_SIZE:
                next_generation.append(child2)

        population = next_generation

# Run the genetic algorithm
if __name__ == "__main__":
    genetic_algorithm()
