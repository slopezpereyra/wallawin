"""Defines all classes and functionality regarding to environmental simulation.
It's where the magic happens."""

import copy
from random import uniform
from math import floor, dist
from matplotlib import pyplot
from matplotlib.patches import Circle
from orgs import Organism
from global_settings import ENV_SETTINGS, PLOT_SETTINGS


class Food:
    """Definse a Food object which the organisms can consume."""

    def __init__(self):
        self.pos = [uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])]


class Environment:
    """Defines an Environment object.

    The environment will be the abstract space in which
    the evolution process will occur. As such it takes a

    Attributes
    ----------
    generation : Generation
        a Generation object to populate the environment
    abundance : float
        a factor to indicate the amount of food f in relation to the population number p. If
        abundance = 1 then f = p. In general, f = a * p
    risk : float
        the chance of environmental death for the organism. Default is 0.
        """

    def __init__(self, pop_size, abundance, risk=0):
        """Self.abundance is a factor multiplied to the size of the population
        to determine the amount of food. If abundance is 1, then food amount will
        be equal to pop size. Over one is excess, below scarcety."""

        self.pop_size = pop_size
        self.generation = self.gen_population(self.pop_size)
        self.risk = risk
        self.abundance = abundance
        self.food = self.gen_food()

    def gen_food(self):
        """Generate the food in the environment."""

        food = [Food() for x in range(0, floor(self.pop_size * self.abundance))]
        return food

    @staticmethod
    def gen_population(size):

        population = [Organism() for x in range(0, size)]
        return population

    def simulate(self):
        """Simulate the evolution process.

        It simulates evolution for as many steps as defined in ENVIRONMENTAL_SETTINGS.
        On each simulation:
            a) it plots the environment on the particular step of the simulation,
            with all its organisms and food particles.
            b) Loops through the organisms and either evolves them if there's no more food in the environment
            or makes them compete for the available food if there's any.

        It evolves them by using the evolve method."""

        simulating, step, gen = True, 0, 0

        while simulating:

            if PLOT_SETTINGS['PLOT'] is True:
                self.plot_step(step, gen)

            for org in self.generation:
                if not self.food:
                    self.evolve()
                    gen += 1

                nearest_food = org.find_food(self.food)
                if dist(org.pos, nearest_food.pos) < 1:
                    org.meals += 1
                    self.food.remove(nearest_food)
                    del nearest_food
                else:
                    org.update_pos(nearest_food.pos)
            step += 1
            print(step)
            if step >= ENV_SETTINGS['STEPS']:
                simulating = False

    def fitness_function(self, org):
        """Sets fitness of an organism according to the amount of food they ate.
        If organism ate two or more food particles it creates a copy of itself,
        which has a chance of mutating.
        If organism didn't succed at getting any particle, it dies.
        Otherwise it just survives.

        Parameters
        ---------
        org : Organism
            The organism to be evaluated as fit or unfit.
        """

        if org.meals >= 2:
            chiral = copy.deepcopy(org)
            chiral.pos = org.start_pos
            if uniform(0, 100) <= ENV_SETTINGS['MUTATION_CHANCE']:
                chiral.mutate()
            self.generation.append(chiral)
        elif org.meals == 0:
            self.generation.remove(org)
            del org
        pass

    def evolve(self):
        """Applies fitness function to every organism on the population
        and then resets the environment (a new day begins!) by getting
        all organisms to their original starting positions and generating
        new food."""

        for index in range(len(self.generation)):
            org = self.generation[index]
            self.fitness_function(org)  # Create double if ate 2 or more, preserve if ate 1, kill if 0.
            org.pos = org.start_pos  # Restart position
            self.food = self.gen_food()  # Regenerate the food

    def plot_step(self, step_num, gen_num):
        """Function that plots a particular step of the evolutionary simulation."""

        figure, axis = pyplot.subplots()
        figure.set_size_inches(9.6, 5.4)

        pyplot.xlim(PLOT_SETTINGS['X_MIN'], PLOT_SETTINGS['X_MAX'])
        pyplot.ylim(PLOT_SETTINGS['Y_MIN'], PLOT_SETTINGS['Y_MAX'])

        for organism in self.generation:
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

        pyplot.figtext(0.025, 0.95, r'GENERATION: ' + str(gen_num))
        pyplot.figtext(0.025, 0.90, r'T_STEP: ' + str(step_num))

        pyplot.savefig('step {}.png'.format(step_num), dpi=100)

    def __str__(self):

        str = """
        Population size: {}
        Food amount: {}""".format(self.pop_size, len(self.food))

        return str


env = Environment(ENV_SETTINGS['POP_SIZE'], 2, 1)

print(env)
env.simulate()
