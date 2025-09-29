import numpy as np

class GreyWolfOptimizer:
    def __init__(self, obj_func, dim, lb, ub, population_size=20, max_iter=100):
        self.obj_func = obj_func
        self.dim = dim
        self.lb = lb
        self.ub = ub
        self.population_size = population_size
        self.max_iter = max_iter
        self.positions = np.random.uniform(lb, ub, (population_size, dim))
        self.alpha_pos = np.zeros(dim)
        self.alpha_score = float("inf")
        self.beta_pos = np.zeros(dim)
        self.beta_score = float("inf")
        self.delta_pos = np.zeros(dim)
        self.delta_score = float("inf")

    def optimize(self):
        for t in range(self.max_iter):
            for i in range(self.population_size):
                self.positions[i] = np.clip(self.positions[i], self.lb, self.ub)
                fitness = self.obj_func(self.positions[i])
                if fitness < self.alpha_score:
                    self.alpha_score = fitness
                    self.alpha_pos = self.positions[i].copy()
                elif fitness < self.beta_score:
                    self.beta_score = fitness
                    self.beta_pos = self.positions[i].copy()
                elif fitness < self.delta_score:
                    self.delta_score = fitness
                    self.delta_pos = self.positions[i].copy()

            a = 2 - t * (2 / self.max_iter)

            for i in range(self.population_size):
                for d in range(self.dim):
                    r1 = np.random.rand()
                    r2 = np.random.rand()
                    A1 = 2 * a * r1 - a
                    C1 = 2 * r2
                    D_alpha = abs(C1 * self.alpha_pos[d] - self.positions[i][d])
                    X1 = self.alpha_pos[d] - A1 * D_alpha

                    r1 = np.random.rand()
                    r2 = np.random.rand()
                    A2 = 2 * a * r1 - a
                    C2 = 2 * r2
                    D_beta = abs(C2 * self.beta_pos[d] - self.positions[i][d])
                    X2 = self.beta_pos[d] - A2 * D_beta

                    r1 = np.random.rand()
                    r2 = np.random.rand()
                    A3 = 2 * a * r1 - a
                    C3 = 2 * r2
                    D_delta = abs(C3 * self.delta_pos[d] - self.positions[i][d])
                    X3 = self.delta_pos[d] - A3 * D_delta

                    self.positions[i][d] = (X1 + X2 + X3) / 3

        return self.alpha_pos, self.alpha_score

def sphere_function(x):
    return sum(x**2)

if __name__ == "__main__":
    dim = 5
    lb = -10
    ub = 10
    gwo = GreyWolfOptimizer(obj_func=sphere_function, dim=dim, lb=lb, ub=ub, population_size=30, max_iter=100)
    best_pos, best_score = gwo.optimize()
    print("Best position:", best_pos)
    print("Best score:", best_score)
