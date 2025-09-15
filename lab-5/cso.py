import numpy as np

def cuckoo_search_knapsack(nests, max_iterations, W_max, items, n_items):
    # Initialize nests (solutions) randomly
    population = np.random.randint(2, size=(nests, n_items))  # 0/1 for knapsack inclusion
    
    # Fitness function
    def fitness(solution):
        total_value = np.sum(solution * items[:, 0])
        total_weight = np.sum(solution * items[:, 1])
        if total_weight > W_max:
            return -np.inf  # Penalty if over capacity
        else:
            return total_value
    
    # Initialize the best solution
    best_solution = None
    best_value = -np.inf
    
    for _ in range(max_iterations):
        for i in range(nests):
            # Generate a new solution using Levy flight
            new_solution = levy_flight(population[i])
            
            # Calculate the fitness of the new solution
            new_value = fitness(new_solution)
            
            # If new solution is better, replace the old one
            if new_value > fitness(population[i]):
                population[i] = new_solution
            
            # Update the best solution found
            if new_value > best_value:Z
                best_value = new_value
                best_solution = new_solution
        
        # Optionally, abandon a fraction of solutions randomly (e.g. 10%)
        abandon_fraction = 0.1
        if np.random.rand() < abandon_fraction:
            rand_idx = np.random.choice(range(nests))
            population[rand_idx] = np.random.randint(2, size=n_items)
    
    return best_solution, best_value

def levy_flight(solution):
    # Generate a new solution based on Levy flight
    step_size = np.random.normal(0, 1, size=solution.shape)
    return np.clip(solution + step_size, 0, 1)

# Example
n_items = 5
items = np.array([[20, 2], [5, 3], [10, 5], [40, 10], [30, 6]])  # (value, weight)
W_max = 10
nests = 50
max_iterations = 100

best_solution, best_value = cuckoo_search_knapsack(nests, max_iterations, W_max, items, n_items)
print("Best Solution:", best_solution)
print("Best Value:", best_value)
