"""Defines all classes and functionality regarding to environmental simulation.
It's where the magic happens."""

import copy
from random import uniform, choice, randint
from math import floor, dist
from orgs import Organism, AltruisticGen
from settings import ENV_SETTINGS, PLOT_SETTINGS
from plotter import plot_epoch_data, plot_step
import numpy as np


class Food:
    """Definse a Food object which the organisms can consume."""

    def __init__(self):
        self.pos = [uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])]


class Environment:
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

    def __init__(self, pop_size, abundance, risk=0, rep_factor=40):
        """Self.abundance is a factor multiplied to the size of the population
        to determine the amount of food. If abundance is 1, then food amount will
        be equal to pop size. Over one is excess, below scarcety."""

        self.pop_size = pop_size
        self.rep_factor = rep_factor
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
        pass

    def simulate (self):
        pass

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

        pass

    def __str__(self):

        str = """
        Population size: {}
        Food amount: {}""".format(self.pop_size, len(self.food))

        return str


class DepletionEnvironment (Environment):

    def __init__(self, pop_size, abundance, risk=0):
        super().__init__(pop_size, abundance, risk)

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
            if randint(0, 100) <= ENV_SETTINGS['MUTATION_CHANCE']:
                chiral.mutate()
            self.generation.append(chiral)
        elif org.meals == 0:
            self.generation.remove(org)
            del org
        pass

# Maybe altruistic organisms can give food over a meal amount aboave 2
# to any other organism, which may keep the extra meal for the next epoch?¿?


class AltruismEnvironment (Environment):
    """An Environment in which organisms are potentially altruistic. By default
    half of the population will be altruistic, the other half of it selfish.
    Altruistic organisms will, if the can survive doing so, share a meal with
    other altruistic organisms that failed at getting any on their own.
    Thus they sacrifice reproductive potential in exchange of ensuring
    the survival of another altruistic organisms."""

    def __init__(self, pop_size, abundance, risk=0, rep_factor=40):
        super().__init__(pop_size, abundance, risk, rep_factor)
        self.alt_pop = [x for x in self.generation if x.altruistic]
        self.self_pop = [x for x in self.generation if not x.altruistic]

    @staticmethod
    def gen_population(size):
        half = int(size / 2)
        alt_pop = [AltruisticGen(altruistic=True, velocity=5) for x in range(0, half)]
        self_pop = [AltruisticGen(altruistic=False, velocity=5) for x in range(0, half)]
        return alt_pop + self_pop

    def kill(self, org):
        """Removes object org from generation and deletes it."""
        self.generation.remove(org)
        del org

    def fitness_function(self, org):
        """Evaluate fitness of organism org in relation to the amount of meals it ate. Act according to evaluation such
        that no meals produces death, one meal survival and normal chance of reproduction, two meals survival and
        high chance of reproduction."""

        if org.meals == 0:
            self.kill(org)
            return

        rep_chance = org.meals * self.rep_factor

        if randint(0, 100) <= rep_chance:
            chiral = copy.deepcopy(org)
            chiral.pos = np.array([uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])])
            chiral.age = 0
            if randint(0, 100) <= ENV_SETTINGS['MUTATION_CHANCE']:
                chiral.mutate()
                self.generation.append(chiral)

        if org.age >= ENV_SETTINGS['LONGEVITY']:
            self.kill(org)

        org.pos = org.start_pos
        org.meals = 0

    def sim_food_competition(self, organisms):
        """Simulate competition for food in the environment
        given a list of Organism objects."""

        for org in organisms:
            # Check if org has energy, there's food and org can still eat. In any false case, go to next organism.
            if org.energy <= 0 or not self.food or org.meals >= 2:
                organisms.remove(org)
                continue

            nearest_food = org.find_food(self.food)
            if dist(org.pos, nearest_food.pos) < ENV_SETTINGS['FEADING_RANGE']:
                org.meals += 1
                self.food.remove(nearest_food)
                del nearest_food
            else:
                org.move_to(nearest_food.pos, effortless=True)

    def altruism(self):
        """Simulates altruistic behavior, based on kin-selection, by making altruistic behaviors with
        two meals share one of them with altruistic behaviors with zero meals."""

        fit_for_sharing = [org for org in self.alt_pop if org.meals >= 2]
        fit_for_receiving = [org for org in self.alt_pop if org.meals == 0]

        for org in fit_for_sharing:
            if not fit_for_receiving:
                break
            recipient = choice(fit_for_receiving)
            fit_for_receiving.remove(recipient)
            org.share(recipient)

    def evolve(self):
        """Simulate altruistic behavior and evaluate each organism's fitness.
        Then reset organism's meals attribute and regenerate food in the environment."""

        self.altruism()
        # A graph of the previous epoch population data and new epoch population data would be useful here.
        for org in self.generation:
            org.age += 1
            self.fitness_function(org)

        self.food = self.gen_food()

    def set_epoch_data(self, epoch, epoch_data):
        """Gather generational data for generation of epoch and
        set it into the epoc_data dictionary (used for plotting)."""

        speed_values = [x.velocity for x in self.generation]

        pop_size = len(self.generation)
        avg_speed = sum(speed_values) / pop_size if pop_size != 0 else sum(speed_values) / 1
        abs_altruistic_population = len([x for x in self.generation if x.altruistic])
        abs_selfish_population = len([x for x in self.generation if not x.altruistic])
        epoch_data[epoch] = [pop_size, avg_speed, abs_altruistic_population, abs_selfish_population]

    def simulate(self, runs=1):
        """Simulate the evolution process, plot and save the data for as many runs
        as specified."""

        for run in range(0, runs):

            simulating, step, epoch, run_count = True, 0, 0, 0
            active_individuals = self.generation.copy()
            epoch_data = {}

            while True:
                step += 1
                if step > ENV_SETTINGS['STEPS'] or len(self.generation) == 0:
                    plot_epoch_data(epoch_data, run)
                    self.generation = self.gen_population(ENV_SETTINGS['POP_SIZE'])
                    break

                if PLOT_SETTINGS['PLOT'] is True and step % 5 == 0:
                    plot_step(self.generation, self.food, step, epoch)

                if not active_individuals:
                    self.evolve()
                    epoch += 1
                    active_individuals = self.generation.copy()
                    self.set_epoch_data(epoch, epoch_data)
                    continue

                self.sim_food_competition(active_individuals)


env = AltruismEnvironment(ENV_SETTINGS['POP_SIZE'], 5, 1, rep_factor=50)
env.simulate(5)
