from random import uniform
from math import floor, dist
import numpy as np
from matplotlib import pyplot
from matplotlib.patches import Circle

ENV_SETTINGS = {'ENV_SIZE_X': 10, 'ENV_SIZE_Y': 10, 'SIMULATION_TIME': 50, 'STEP': 1}
PLOT_SETTINGS = {'X_MIN': 0.0, 'X_MAX': 10.0, 'Y_MIN': 0.0, 'Y_MAX': 10.0}


class Organism:

    def __init__(self):
        self.fitness = uniform(0, 1)
        self.altruism = uniform(0, 1)
        self.velocity = 0.5
        self.pos = np.array([uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])])
        self.meals = 0

    def update_pos(self, target_pos):

        delta = target_pos - self.pos
        distance = dist(target_pos, self.pos)
        ratio = self.velocity / distance
        direction = ratio * delta
        self.pos = self.pos + direction

    def find_food(self, food):
        """Return the nearest food in the environment."""

        distances = []
        for f in food:
            d = dist(self.pos, f.pos)
            distances.append(d)

        # Set the target food to be the nearest one.
        target = food[distances.index(min(distances))]
        return target

    def __str__(self):

        str = """
        Organism fitness: {}
        Organism altruism: {}
        Organism velocity: {}
        Organism position: {}
        Organism meals: {}""".format(self.fitness, self.altruism, self.velocity, self.pos, self.meals)

        return str

class Generation:

    def __init__(self, size):

        self.size = size
        self.organisms = self.gen_population(size)
        self.avg_fitness = sum(org.fitness for org in self.organisms) / len(self.organisms)
        self.avg_altruism = sum(org.altruism for org in self.organisms) / len(self.organisms)

    def gen_population(self, equal_distribution=True):

        population = [Organism() for x in range(0, self.size)]
        return population

    def rep_orgs(self):

        for org in self.organisms:
            print(org)

    def __str__(self):

        str = """
        Generation size: {}
        Average fitness: {}
        Average altruism: {}""".format(self.size, self.avg_fitness, self.avg_altruism)

        return str


class Food:

    def __init__(self):
        self.pos = [uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])]


class Environment:

    def __init__(self, population, abundance, risk):
        """Self.abundance is a factor multiplied to the size of the population
        to determine the amount of food. If abundance is 1, then food amount will
        be equal to pop size. Over one is excess, below scarcety."""

        self.population = population
        self.risk = risk
        self.abundance = abundance
        self.food = self.gen_food()

    def gen_food(self):

        food = [Food() for x in range(0, floor(self.population.size * self.abundance))]
        return food

    def simulate(self):

        time_steps = int(ENV_SETTINGS['SIMULATION_TIME'] / ENV_SETTINGS['STEP'])
        print("TIME SETPS ", time_steps)

        for step in range(0, time_steps):

            self.plot_step(step)
            for org in self.population.organisms:
                nearest_food = org.find_food(self.food)
                if dist(org.pos, nearest_food.pos) < 1:
                    org.meals += 1
                    self.food.remove(nearest_food)
                    del nearest_food
                else:
                    org.update_pos(nearest_food.pos)

    def plot_step(self, step_num):
        figure, axis = pyplot.subplots()
        figure.set_size_inches(9.6, 5.4)

        pyplot.xlim(PLOT_SETTINGS['X_MIN'], PLOT_SETTINGS['X_MAX'])
        pyplot.ylim(PLOT_SETTINGS['Y_MIN'], PLOT_SETTINGS['Y_MAX'])

        for organism in self.population.organisms:
            print("Printing organism at ", organism.pos)
            org_circle = Circle(organism.pos, 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
            edge = Circle(organism.pos, 0.05, facecolor='None', edgecolor='darkgreen', zorder=8)
            axis.add_patch(org_circle)
            axis.add_patch(edge)
        for food in self.food:
            food_circle = Circle(food.pos, 0.03, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
            axis.add_patch(food_circle)

        axis.set_aspect('equal')
        frame = pyplot.gca()
        frame.axes.get_xaxis().set_ticks([])
        frame.axes.get_yaxis().set_ticks([])

        pyplot.figtext(0.025, 0.95, r'GENERATION: ')
        pyplot.figtext(0.025, 0.90, r'T_STEP: ' + str(step_num))

        pyplot.savefig('step {}.png'.format(step_num), dpi=100)

    def __str__(self):

        str = """
        Population size: {}
        Food amount: {}""".format(self.population.size, len(self.food))

        return str


env = Environment(Generation(1), 5, 1)

print(env)
env.simulate()
