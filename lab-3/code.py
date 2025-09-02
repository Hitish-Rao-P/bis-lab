
import numpy as np

def sphere_function(x):
    return np.sum(x ** 2)

class Particle:
    def __init__(self, dim, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], dim)
        self.velocity = np.zeros(dim)
        self.best_position = np.copy(self.position)
        self.best_score = float('inf')

    def evaluate(self, objective_func):
        score = objective_func(self.position)
        if score < self.best_score:
            self.best_score = score
            self.best_position = np.copy(self.position)

    def update_velocity(self, global_best, w, c1, c2):
        r1 = np.random.rand(len(self.position))
        r2 = np.random.rand(len(self.position))
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best - self.position)
        self.velocity = w * self.velocity + cognitive + social

    def update_position(self, bounds):
        self.position += self.velocity
        self.position = np.clip(self.position, bounds[0], bounds[1])

def pso(objective_func, dim, num_particles, max_iter, bounds,
        w=0.5, c1=1.5, c2=1.5):
    
    swarm = [Particle(dim, bounds) for _ in range(num_particles)]
    global_best_position = np.random.uniform(bounds[0], bounds[1], dim)
    global_best_score = float('inf')
    
    for iter in range(max_iter):
        for particle in swarm:
            particle.evaluate(objective_func)
            
            if particle.best_score < global_best_score:
                global_best_score = particle.best_score
                global_best_position = np.copy(particle.best_position)
        
        for particle in swarm:
            particle.update_velocity(global_best_position, w, c1, c2)
            particle.update_position(bounds)
        
        print(f"Iteration {iter+1}/{max_iter}, Best Score: {global_best_score:.5f}")
    
    return global_best_position, global_best_score

if __name__ == "__main__":
    dim = 5  
    num_particles = 5
    max_iter = 5
    bounds = (-10, 10)
    
    best_pos, best_score = pso(sphere_function, dim, num_particles, max_iter, bounds)
    
    print("\nBest position found:", best_pos)
    print("Best score:", best_score)
