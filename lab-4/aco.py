import numpy as np

# Problem definition
items = [
    {"value": 60, "weight": 10},
    {"value": 100, "weight": 20},
    {"value": 120, "weight": 30},
]

capacity = 50
num_items = len(items)

# Parameters for ACO
num_ants = 10
num_iterations = 50
alpha = 1.0    # Influence of pheromone
beta = 2.0     # Influence of heuristic (value/weight)
evaporation_rate = 0.5
pheromone_init = 1.0

# Initialize pheromone levels on items
pheromones = np.full(num_items, pheromone_init)

def fitness(solution):
    total_value = 0
    total_weight = 0
    for i in range(num_items):
        if solution[i] == 1:
            total_value += items[i]["value"]
            total_weight += items[i]["weight"]
    if total_weight > capacity:
        return 0
    return total_value

def construct_solution(pheromones):
    solution = np.zeros(num_items, dtype=int)
    total_weight = 0

    for i in range(num_items):
        # Calculate desirability = pheromone^alpha * heuristic^beta
        heuristic = items[i]["value"] / items[i]["weight"]
        desirability = (pheromones[i] ** alpha) * (heuristic ** beta)

        # Probability to include the item proportional to desirability
        prob = desirability / (desirability + 1)  # simple probability model

        if np.random.rand() < prob:
            if total_weight + items[i]["weight"] <= capacity:
                solution[i] = 1
                total_weight += items[i]["weight"]
            else:
                solution[i] = 0  # cannot add due to weight limit
        else:
            solution[i] = 0

    return solution

def update_pheromones(pheromones, solutions, fitnesses):
    # Evaporate pheromones
    pheromones *= (1 - evaporation_rate)

    # Add pheromone proportional to fitness for selected items
    for sol, fit in zip(solutions, fitnesses):
        for i in range(num_items):
            if sol[i] == 1:
                pheromones[i] += fit

def ant_colony_optimization():
    global pheromones
    best_solution = None
    best_fitness = 0

    for iteration in range(num_iterations):
        solutions = []
        fitnesses = []

        for _ in range(num_ants):
            sol = construct_solution(pheromones)
            fit = fitness(sol)
            solutions.append(sol)
            fitnesses.append(fit)

            if fit > best_fitness:
                best_solution = sol
                best_fitness = fit

        update_pheromones(pheromones, solutions, fitnesses)
        print(f"Iteration {iteration+1}: Best Fitness = {best_fitness}")

    return best_solution, best_fitness

# Run the ACO algorithm
best_solution, best_value = ant_colony_optimization()

print("\nBest solution found:", best_solution)
print("Total value of selected items:", best_value)
