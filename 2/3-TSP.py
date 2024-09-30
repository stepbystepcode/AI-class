import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Generate coordinates for 10 random cities
NUM_CITIES = 10
cities = np.random.rand(NUM_CITIES, 2) * 100

# Calculate the Euclidean distance matrix between cities
distance_matrix = np.zeros((NUM_CITIES, NUM_CITIES))
for i in range(NUM_CITIES):
    for j in range(NUM_CITIES):
        if i != j:
            distance_matrix[i][j] = math.sqrt((cities[i][0] - cities[j][0]) ** 2 + (cities[i][1] - cities[j][1]) ** 2)

# Parameter settings
POP_SIZE = 100  # Population size
GENERATIONS = 500  # Number of generations
CROSSOVER_RATE = 0.8  # Crossover probability
MUTATION_RATE = 0.02  # Mutation probability
ELITE_SIZE = 1  # Number of elites to keep

# Initialize the population
def initialize_population(pop_size, num_cities):
    population = []
    for _ in range(pop_size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# Calculate the path length
def calculate_fitness(individual, distance_matrix):
    total_distance = 0
    for i in range(len(individual)):
        from_city = individual[i]
        to_city = individual[(i + 1) % len(individual)]
        total_distance += distance_matrix[from_city][to_city]
    return total_distance

# Selection operation: Roulette wheel selection
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selection_probs = [fitness / total_fitness for fitness in fitness_scores]
    selected_index = np.random.choice(len(population), size=2, replace=False, p=selection_probs)
    return [population[selected_index[0]], population[selected_index[1]]]

# Crossover operation: Order crossover (OX)
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child_p1 = parent1[start:end]
        child_p2 = [item for item in parent2 if item not in child_p1]
        child = child_p2[:start] + child_p1 + child_p2[start:]
        return child
    else:
        return parent1.copy()

# Mutation operation: Swap mutation
def mutate(individual):
    for swapped in range(len(individual)):
        if random.random() < MUTATION_RATE:
            swap_with = random.randint(0, len(individual) - 1)
            individual[swapped], individual[swap_with] = individual[swap_with], individual[swapped]
    return individual

# Elitism
def elitism(population, fitness_scores, elite_size):
    sorted_indices = np.argsort(fitness_scores)
    elites = [population[i] for i in sorted_indices[:elite_size]]
    return elites

# Main genetic algorithm
def genetic_algorithm():
    population = initialize_population(POP_SIZE, NUM_CITIES)
    best_distance = float('inf')
    best_path = None
    history = []

    for generation in range(GENERATIONS):
        # Calculate fitness
        fitness_scores = [calculate_fitness(ind, distance_matrix) for ind in population]
        
        # Record the best individual
        min_distance = min(fitness_scores)
        if min_distance < best_distance:
            best_distance = min_distance
            best_path = population[fitness_scores.index(min_distance)]
        
        history.append(best_distance)
        
        # Elitism
        elites = elitism(population, fitness_scores, ELITE_SIZE)
        
        # Generate a new population
        new_population = elites.copy()
        while len(new_population) < POP_SIZE:
            parents = selection(population, fitness_scores)
            child = crossover(parents[0], parents[1])
            child = mutate(child)
            new_population.append(child)
        
        population = new_population
    
    return best_path, best_distance, history

# Run the genetic algorithm
best_path, best_distance, history = genetic_algorithm()

# Output the results
print("Best path length: {:.2f}".format(best_distance))
print("Best path: ", best_path)

# Visualize the results
plt.figure(figsize=(10, 5))

# Plot the city distribution
plt.subplot(1, 2, 1)
plt.scatter(cities[:, 0], cities[:, 1], color='red')
for i, (x, y) in enumerate(cities):
    plt.text(x + 1, y + 1, str(i), fontsize=12)
# Plot the best path
path = best_path + [best_path[0]]
path_coords = cities[path]
plt.plot(path_coords[:, 0], path_coords[:, 1], linestyle='-', color='blue')
plt.title('Best Path Illustration')

# Plot the fitness change
plt.subplot(1, 2, 2)
plt.plot(history, color='green')
plt.title('Fitness Change')
plt.xlabel('Generation')
plt.ylabel('Path Length')

plt.tight_layout()
plt.show()
