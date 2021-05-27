"""Defines all classes and functionality regarding to environmental simulation.
It's where the magic happens."""

from random import uniform, randint
from math import floor, dist
from wallawin.src.data_representation import save_simulation_settings
import os


class Food:
    """Definse a Food object which the organisms can consume."""

    def __init__(self, pos):
        self.pos = pos


class BaseSimulator:
    """Base class for all Simulator objects.
    The Simulator will be the abstract space in which
    the evolution process will occur.

    Attributes
    ----------
    sim_settings: Settings
        a Settings object that defines the population size, abundance of food,
        base mutation chance, base mutability, feading range of the organisms
        (for simulations involving movement) and longevity.
        """

    def __init__(self, sim_settings):
        """Simulator object. Simulates the whole evolutionary process. Takes
        a Settings object as argument."""

        self.settings = sim_settings
        self.env_size = [self.settings.env_size_x, self.settings.env_size_y]
        self.generation = self.gen_population(sim_settings.pop_size)
        self.food = self.gen_food()
        self.data = {}

        os.mkdir('data/{}'.format(self.settings.simulation_name))
        save_simulation_settings(self.settings, self.settings.simulation_name)

    def gen_food(self):
        """Generate the food in the environment. If the food generation is static, then the same amount of food will
            be generated on each step of the simulation. Otherwise the amount of food generated will be
            proportional to the population number according to the abundance factor of the settings.
       """

        if self.settings.static_food_generation:
            food = [Food([uniform(0, self.settings.env_size_x), uniform(0, self.settings.env_size_y)])
                    for x in range(0, floor(self.settings.pop_size * self.settings.abundance))]
        else:
            food = [Food([uniform(0, self.settings.env_size_x), uniform(0, self.settings.env_size_y)])
                    for x in range(0, floor(len(self.generation) * self.settings.abundance))]

        return food

    def gen_population(self, size):
        """Base method for population generation."""
        pass

    def simulate (self):
        """Base method to begin simulation."""
        pass

    def kill(self, org):
        """Removes object org from generation and deletes it.

        Parameters
        ----------
        org : Organism
            The organism to be deleted of the current generation."""

        self.generation.remove(org)
        del org

    def fitness_function(self, org):
        """Base method to stablish whether an organism is fit or not; i.e., if it will survive and
        what its chance of reproducing is if that is the case.

        Parameters
        ----------
        org: Organism
            The organism whose fitness is to be evaluated."""
        pass

    def sim_competition(self, organisms):
        """Base method to simulate the competition for food among a group of organisms.

        Parameters
        ----------
        organisms : list
            A list of objects of type Organism that will compete with each other."""
        pass

    def __str__(self):

        str = """
        Population size: {}
        Food amount: {}""".format(self.settings.pop_size, len(self.food))

        return str
