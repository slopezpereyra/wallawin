import copy
from wallawin.src.base_simulator import BaseSimulator
from random import randint
from math import dist
from wallawin.src.orgs import BaseOrganism
from wallawin.src.settings import SIM_SETTINGS, PLOT_SETTINGS


class DepletionEnvironment (BaseSimulator):
    """Basic simulation. Organisms compite in a two-dimensional world for food.
    After the food is done or everyone ate two meals, natural selection is applied
    and a new offspring generated."""

    def __init__(self, settings):
        super().__init__(settings)

    @staticmethod
    def gen_population(size):

        population = [BaseOrganism() for x in range(0, size)]
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
        org : BaseOrganism
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