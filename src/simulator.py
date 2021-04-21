"""Defines all classes and functionality regarding to environmental simulation.
It's where the magic happens."""

import copy
from random import uniform, randint
from math import floor, dist
from orgs import Organism
from settings import SIM_SETTINGS, PLOT_SETTINGS


class Food:
    """Definse a Food object which the organisms can consume."""

    def __init__(self):
        self.pos = [uniform(0, SIM_SETTINGS['ENV_SIZE_X']), uniform(0, SIM_SETTINGS['ENV_SIZE_Y'])]


class Simulator:
    """Defines an Environment object.
    The environment will be the abstract space in which
    the evolution process will occur. As such it takes
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

    def __init__(self, settings):
        """Simulator object. Simulates the whole evolutionary process. Takes
        a Settings object as argument."""

        self.settings = settings
        self.generation = self.gen_population(settings.pop_size)
        self.food = self.gen_food()

    def gen_food(self, static=True):
        """Generate the food in the environment."""
        if static:
            food = [Food() for x in range(0, floor(self.settings.pop_size * self.settings.abundance))]
        else:
            food = [Food() for x in range(0, floor(len(self.generation) * self.settings.abundance))]
        return food

    @staticmethod
    def gen_population(size):
        pass

    def simulate (self):
        pass

    def kill(self, org):
        """Removes object org from generation and deletes it."""
        self.generation.remove(org)
        del org

    def fitness_function(self, org):
        pass

    def sim_competition(self, organisms):
        pass

    def __str__(self):

        str = """
        Population size: {}
        Food amount: {}""".format(self.settings.pop_size, len(self.food))

        return str


class DepletionEnvironment (Simulator):

    def __init__(self, settings):
        super().__init__(settings)

    @staticmethod
    def gen_population(size):

        population = [Organism() for x in range(0, size)]
        return population

    def evolve(self):

        for index in range(len(self.generation)):
            org = self.generation[index]
            self.fitness_function(org)  # Create double if ate 2 or more, preserve if ate 1, kill if 0.
            org.pos = org.start_pos  # Restart position
            self.food = self.gen_food()  # Regenerate the food

    def simulate(self):
        """Simulate the evolution process where reproduction occurs
        after organisms compete for food and all food is depleted.
        Simulation lasts for as many steps as defined in ENVIRONMENTAL_SETTINGS.
        On each simulation:
            a) if PLOT_SETTINGS['PLOT'] is true, plots the environment on the particular step of the simulation.
            b) Loop through the organisms making them compete for the available food.
            c) If all food has been consumed, apply natural selection.
            d) Reset position of the organisms, create more food and start again.
        """

        simulating, step, gen = True, 0, 0

        while simulating:

            if PLOT_SETTINGS['PLOT'] is True:
                self.plot_step(step, gen)

            for org in self.generation:
                if not self.food:  # If the organisms ate all the available food
                    self.evolve()
                    gen += 1

                nearest_food = org.find_food(self.food)
                if dist(org.pos, nearest_food.pos) < 1:
                    org.meals += 1
                    self.food.remove(nearest_food)
                    del nearest_food
                else:
                    org.move_to(nearest_food.pos)
            step += 1

            if step >= SIM_SETTINGS['STEPS']:
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
            if randint(0, 100) <= self.settings.mutation_chance:
                chiral.mutate()
            self.generation.append(chiral)
        elif org.meals == 0:
            self.generation.remove(org)
            del org
        pass

# Maybe altruistic organisms can give food over a meal amount aboave 2
# to any other organism, which may keep the extra meal for the next epoch?¿?

