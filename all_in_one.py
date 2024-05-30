import math
import random
import matplotlib.pyplot as plt

class City:
    def __init__(self, x=None, y=None):
        if x is None and y is None:
            self.x = random.randint(0, 200)
            self.y = random.randint(0, 200)
        else:
            self.x = x
            self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distanceTo(self, city):
        xDistance = abs(self.getX() - city.getX())
        yDistance = abs(self.getY() - city.getY())
        distance = math.sqrt(xDistance ** 2 + yDistance ** 2)
        return distance
    
    def __str__(self):
        return f"{self.getX()}, {self.getY()}"

class TourManager:
    destinationCities = []

    @staticmethod
    def addCity(city):
        TourManager.destinationCities.append(city)

    @staticmethod
    def getCity(index):
        return TourManager.destinationCities[index]

    @staticmethod
    def numberOfCities():
        return len(TourManager.destinationCities)

class Tour:
    def __init__(self):
        self.tour = [None] * TourManager.numberOfCities()
        self.fitness = 0
        self.distance = 0

    def generateIndividual(self):
        for cityIndex in range(TourManager.numberOfCities()):
            self.setCity(cityIndex, TourManager.getCity(cityIndex))
        random.shuffle(self.tour[1:])

    def getCity(self, tourPosition):
        return self.tour[tourPosition]

    def setCity(self, tourPosition, city):
        self.tour[tourPosition] = city
        self.fitness = 0
        self.distance = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / self.getDistance()
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for cityIndex in range(self.tourSize()):
                fromCity = self.getCity(cityIndex)
                if cityIndex + 1 < self.tourSize():
                    destinationCity = self.getCity(cityIndex + 1)
                else:
                    destinationCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(destinationCity)
            self.distance = tourDistance
        return self.distance

    def tourSize(self):
        return len(self.tour)

    def containsCity(self, city):
        return city in self.tour

    def __str__(self):
        geneString = "|"
        for city in self.tour:
            geneString += str(city) + "|"
        return geneString

class GA:
    mutationRate = 0.015
    tournamentSize = 5
    elitism = True

    @staticmethod
    def evolvePopulation(pop):
        newPopulation = Population(pop.populationSize(), initialise=False)

        elitismOffset = 0
        if GA.elitism:
            newPopulation.saveTour(0, pop.getFittest())
            elitismOffset = 1

        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = GA.tournamentSelection(pop)
            parent2 = GA.tournamentSelection(pop)
            child = GA.crossover(parent1, parent2)
            newPopulation.saveTour(i, child)

        for i in range(elitismOffset, newPopulation.populationSize()):
            GA.mutate(newPopulation.getTour(i))

        return newPopulation

    @staticmethod
    def crossover(parent1, parent2):
        child = Tour()

        startPos = random.randint(0, parent1.tourSize() - 1)
        endPos = random.randint(0, parent1.tourSize() - 1)

        for i in range(1, child.tourSize()):
            if startPos < endPos and startPos < i < endPos:
                child.setCity(i, parent1.getCity(i))
            elif startPos > endPos:
                if not (endPos < i < startPos):
                    child.setCity(i, parent1.getCity(i))

        for i in range(1, parent2.tourSize()):
            if not child.containsCity(parent2.getCity(i)):
                for ii in range(1, child.tourSize()):
                    if child.getCity(ii) is None:
                        child.setCity(ii, parent2.getCity(i))
                        break

        child.setCity(0, parent1.getCity(0))
        return child

    @staticmethod
    def mutate(tour):
        for tourPos1 in range(1, tour.tourSize()):
            if random.random() < GA.mutationRate:
                tourPos2 = random.randint(1, tour.tourSize() - 1)
                city1 = tour.getCity(tourPos1)
                city2 = tour.getCity(tourPos2)
                tour.setCity(tourPos2, city1)
                tour.setCity(tourPos1, city2)

    @staticmethod
    def tournamentSelection(pop):
        tournament = Population(GA.tournamentSize, initialise=False)
        for i in range(GA.tournamentSize):
            randomId = random.randint(0, pop.populationSize() - 1)
            tournament.saveTour(i, pop.getTour(randomId))
        return tournament.getFittest()

class Population:
    def __init__(self, populationSize, initialise=True):
        self.tours = [None] * populationSize
        if initialise:
            for i in range(populationSize):
                newTour = Tour()
                newTour.generateIndividual()
                self.saveTour(i, newTour)

    def saveTour(self, index, tour):
        self.tours[index] = tour

    def getTour(self, index):
        return self.tours[index]

    def getFittest(self):
        fittest = self.tours[0]
        for i in range(1, self.populationSize()):
            if fittest.getFitness() <= self.getTour(i).getFitness():
                fittest = self.getTour(i)
        return fittest

    def populationSize(self):
        return len(self.tours)

def two_opt(route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                if route[i-1].distanceTo(route[j-1]) + route[i].distanceTo(route[j]) < route[i-1].distanceTo(route[i]) + route[j-1].distanceTo(route[j]):
                    route[i:j] = reversed(route[i:j])
                    improved = True
                    best = route
    return best

def plot_tour(tour, first):
    if first == True:
        title = "Initial tour"
    else:
        title = "Optimized tour"

    x_values = [city.getX() for city in tour]
    y_values = [city.getY() for city in tour]

    plt.plot(x_values + [x_values[0]], y_values + [y_values[0]], 'b-')
    plt.plot(x_values, y_values, 'ro')
    plt.plot(x_values[0], y_values[0], 'go', markersize=10)

    for i, city in enumerate(tour):
        plt.text(city.getX(), city.getY(), f"{i}", fontsize=8, va='bottom')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'{title}')
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f"{title}.png")
    plt.show()

if __name__ == "__main__":
    cities = [
        City(60, 200),
        City(180, 200),
        City(80, 180),
        City(140, 180),
        City(20, 160),
        City(100, 160),
        City(200, 160),
        City(140, 140),
        City(40, 120),
        City(100, 120),
        City(180, 100),
        City(60, 80),
        City(120, 80),
        City(180, 60),
        City(20, 40),
        City(100, 40),
        City(200, 40),
        City(20, 20),
        City(60, 20),
        City(160, 20)
    ]
    for city in cities:
        TourManager.addCity(city)

    all_distances = []

    pop = Population(50, initialise=True)
    print("Initial distance:", pop.getFittest().getDistance())
    initial_pop = pop.getFittest()
    plot_tour(initial_pop.tour, True)

    for _ in range(100):
        pop = GA.evolvePopulation(pop)
        all_distances.append(pop.getFittest().getDistance())

    best_tour = pop.getFittest().tour
    best_tour = two_opt(best_tour)
    print("Finished")
    print("Final distance:", pop.getFittest().getDistance())
    print("Solution:")
    print(pop.getFittest())

    plot_tour(best_tour, False)

    plt.plot(all_distances)
    plt.xlabel('pop')
    plt.ylabel('distance')
    plt.title('distance')
    plt.grid(True)
    plt.savefig("distance.png")
    plt.show()
