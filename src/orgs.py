"""Organisms' traits and behavior."""

from random import uniform, getrandbits
from math import dist
import numpy as np
from wallawin.src.settings import SIM_SETTINGS


class BaseOrganism:
    """Defines an organism object capable of interacting with an environment,
    eating, reproducing and dying.

    Attributes
    ----------
    longevity : int
        How many steps will this organism live before dying of old age?
    energy : float
        Amount of energy available to spend in search for food each step. Only
        relevant in simulations involving movement.
    energy_release : float
        A factor determining how quickly the energy is released.
        Energy release is always proportionally equivalent to velocity.
        Only relevant in simulations involving movement.
    velocity : float
        Distance covered by the individual in a single evolutionary step.
        Default value is random between 1 and 2.
        Only relevant in simulations involving movement.
    pos : array
        An array serving as a two-dimensional vector. Represents x y coordinates
        of the organism's position. Random value asigned on initialization.
    start_pos : array
        The starting position of the organism.
    meals : int
        Amount of food particles consumed by the organism in each evolutionary step."""

    def __init__(self, traits):
        self.traits = traits
        self.pos = np.array([uniform(0, SIM_SETTINGS['ENV_SIZE_X']), uniform(0, SIM_SETTINGS['ENV_SIZE_Y'])])
        self.start_pos = self.pos
        self.meals = 0
        self.age = 0

    def move_to(self, target_pos, effortless=False):
        """Move the organism towards the target_pos and consume
        energy.

        Parameters
        ----------
        target_pos : array
            A two dimensional x, y vector representing the position the organism must move to.
        effortless : bool
            Set to False by default. If true the organism will not waste energy moving. Useful
            for certain simulations."""

        if self.traits.energy > 0:
            delta = target_pos - self.pos
            distance = dist(target_pos, self.pos)
            ratio = self.traits.velocity / distance
            direction = ratio * delta
            self.pos = self.pos + direction
            if not effortless:
                # More velocity, more energy release.
                self.traits.energy -= self.traits.velocity * self.traits.energy_release

    def find_food(self, food):
        """Return the nearest food in the simulation.

        Parameters
        ----------
        food : list
            All food particles currently existing on the simulation."""

        distances = []
        for f in food:
            d = dist(self.pos, f.pos)
            distances.append(d)

        # Set the target food to be the nearest one.
        target = food[distances.index(min(distances))]
        return target

    def mutate(self):
        """Mutate the altruism, velocity or both depending on a random choice."""

        a = range(0, 1)
        #if a == 1:
            #self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])

    def __str__(self):

        str = """
        Organism velocity: {}
        Organism position: {}
        Organism meals: {}""".format(self.traits.velocity, self.pos, self.meals)

        return str


class AltruisticOrganism (BaseOrganism):

    """ Attributes
    ----------
    velocity : float
        Velocity of the organism. Randomly assigned on initialization.
    altruistic : bool
        Determines whether organism is altruistic or not.
    shared : bool
        Set to false on initialization. Represents whether this organism
        has altruistically shared food with another or not on the current
        step of the simulation.
    received_from : list
        List of organisms that shared their food with this organism.
    shared_to : list
        List of organisms that received food from this organism.
        """

    def __init__(self, traits):
        super().__init__(traits)
        self.shared = False
        self.received_from = []  # For future implementation of reciprocity mechanisms, for the moment useless.
        self.shared_to = []
        self.food = None

    def share(self, recipient):
        """Shares food particle with recipient organism.

        Parameters
        ----------
        recipient : Organism
            The organism that will receive a food particle from this one."""

        recipient.meals += 1
        self.meals -= 1
        self.shared = True
        self.shared_to.append(recipient)
        recipient.received_from.append(self)

    def mutate(self):

        #self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])
        pass

    def __str__(self):

        str = """
        Organism is altruistic: {}
        Organism velocity: {}
        Organism position: {}
        Organism meals: {}""".format(self.traits.altruistic, self.traits.velocity, self.pos, self.meals)

        return str