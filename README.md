# Travelling Salesman Problem (TSP) Solver with Genetic Algorithm

## Overview
This Python program solves the Travelling Salesman Problem (TSP) using a Genetic Algorithm (GA). The program defines a set of classes and functions to manage cities, tours, populations, and genetic algorithm operations. Additionally, it includes visualization functions to plot the initial and optimized tours.

## Classes

### 1. City
Represents a city with x and y coordinates. It includes methods to get coordinates and calculate the distance to another city.

- **Methods**:
  - `__init__(self, x=None, y=None)`: Initializes a city with random or specific coordinates.
  - `getX(self)`: Returns the x coordinate.
  - `getY(self)`: Returns the y coordinate.
  - `distanceTo(self, city)`: Calculates the distance to another city.
  - `__str__(self)`: Returns the string representation of the city's coordinates.

### 2. TourManager
Manages the list of destination cities.

- **Methods**:
  - `addCity(city)`: Adds a city to the destination list.
  - `getCity(index)`: Retrieves a city by its index.
  - `numberOfCities()`: Returns the number of cities in the list.

### 3. Tour
Represents a tour (sequence of cities) and includes methods to generate, manipulate, and evaluate tours.

- **Methods**:
  - `__init__(self)`: Initializes an empty tour.
  - `generateIndividual(self)`: Generates a random tour.
  - `getCity(self, tourPosition)`: Returns the city at a specific position in the tour.
  - `setCity(self, tourPosition, city)`: Sets a city at a specific position in the tour.
  - `getFitness(self)`: Calculates and returns the fitness of the tour.
  - `getDistance(self)`: Calculates and returns the total distance of the tour.
  - `tourSize(self)`: Returns the number of cities in the tour.
  - `containsCity(self, city)`: Checks if a city is in the tour.
  - `__str__(self)`: Returns the string representation of the tour.

### 4. Population
Represents a population of tours and includes methods to manage and evolve the population.

- **Methods**:
  - `__init__(self, populationSize, initialise=True)`: Initializes the population.
  - `saveTour(self, index, tour)`: Saves a tour at a specific index.
  - `getTour(self, index)`: Retrieves a tour by its index.
  - `getFittest(self)`: Returns the fittest tour in the population.
  - `populationSize(self)`: Returns the size of the population.

### 5. GA (Genetic Algorithm)
Implements the genetic algorithm operations including crossover, mutation, and selection.

- **Methods**:
  - `evolvePopulation(pop)`: Evolves the population using selection, crossover, and mutation.
  - `crossover(parent1, parent2)`: Performs crossover between two parent tours to produce a child tour.
  - `mutate(tour)`: Mutates a tour.
  - `tournamentSelection(pop)`: Selects a tour from the population using tournament selection.

## Functions

### two_opt(route)
Implements the 2-opt optimization algorithm to improve the tour by reversing segments of the tour.

- **Parameters**:
  - `route`: The initial tour (list of cities).
- **Returns**:
  - `best`: The optimized tour.

### plot_tour(tour, first)
Plots the given tour on a 2D plane.

- **Parameters**:
  - `tour`: The tour to be plotted (list of cities).
  - `first`: Boolean indicating if it's the initial tour (`True`) or optimized tour (`False`).

## Usage

### Initialization and Tour Generation
1. Create a list of cities with specific coordinates.
2. Add cities to the `TourManager`.
3. Initialize a population of tours.
4. Plot the initial tour.

### Evolution and Optimization
1. Evolve the population for a number of generations.
2. Apply the 2-opt optimization to the best tour.
3. Plot the optimized tour.
4. Plot the distance evolution over generations.

### Example

```python
if __name__ == "__main__":
    # Create and add cities
    cities = [City(60, 200), City(180, 200), ...]
    for city in cities:
        TourManager.addCity(city)

    # Initialize population
    pop = Population(50, initialise=True)
    print("Initial distance:", pop.getFittest().getDistance())
    initial_pop = pop.getFittest()
    plot_tour(initial_pop.tour, True)

    # Evolve population
    for _ in range(100):
        pop = GA.evolvePopulation(pop)

    # Optimize the best tour using 2-opt
    best_tour = pop.getFittest().tour
    best_tour = two_opt(best_tour)
    print("Finished")
    print("Final distance:", pop.getFittest().getDistance())
    print("Solution:")
    print(pop.getFittest())

    # Plot optimized tour
    plot_tour(best_tour, False)
```

This example demonstrates the creation of cities, initialization of the population, evolution of the population using GA, optimization using 2-opt, and visualization of the tours.
