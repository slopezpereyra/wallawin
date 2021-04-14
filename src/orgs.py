"""Organisms' traits and behavior."""

from random import uniform, getrandbits
from math import dist
import numpy as np
from global_settings import ENV_SETTINGS


class Organism:
    """Defines an organism object capable of interacting with an environment,
    eating, reproducing and dying.

    Attributes
    ----------
    altruistic : bool
        True if organism is altruistic, False if not
    energy : float
        Amount of energy available to spend in search for food
    energy_release : float
        A factor determining how quickly the energy is released.
        Energy release is always proportionally equivalent to velocity.
    velocity : float
        Distance covered by the individual in a single evolutionary step.
        Default value is random between 1 and 2.
    pos : array
        An array serving as a two-dimensional vector. Represents x y coordinates
        of the organism's position.
    start_pos : array
        The starting position of the organism.
    meals : int
        Amount of food particles consumed by the organism in each evolutionary epoch."""

    def __init__(self, velocity=uniform(0, 0.5)):
        self.energy = 10
        self.energy_release = 0.1
        self.velocity = velocity
        self.pos = np.array([uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])])
        self.start_pos = self.pos
        self.meals = 0

    def move_to(self, target_pos, effortless=False):
        """Move the organism towards the target_pos and consume
        energy."""

        if self.energy > 0:
            delta = target_pos - self.pos
            distance = dist(target_pos, self.pos)
            ratio = self.velocity / distance
            direction = ratio * delta
            self.pos = self.pos + direction
            if effortless is False:
                self.energy -= self.velocity * self.energy_release  # More velocity, more energy release.

    def find_food(self, food):
        """Return the nearest food in the environment."""

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
        if a == 1:
            self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])

    def __str__(self):

        str = """
        Organism velocity: {}
        Organism position: {}
        Organism meals: {}""".format(self.velocity, self.pos, self.meals)

        return str


class AltruisticOrganism (Organism):

    def __init__(self, velocity=uniform(1, 2)):
        super().__init__()
        self.altruism = uniform(0, 1)
        self.shared = False
        self.received_from = []  # For future implementation of reciprocity mechanisms, for the moment useless.
        self.shared_to = []
        self.received_from = []

    def share(self, recipient):

        recipient.meals += 1
        self.meals -= 1
        self.shared = True
        self.shared_to.append(recipient)
        recipient.received_from.append(self)

    def mutate(self):

        a = range(0, 2)
        if a == 0:
            self.altruism *= uniform(1, ENV_SETTINGS['MUTABILITY'])
        elif a == 1:
            self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])
        else:
            self.altruism *= uniform(1, ENV_SETTINGS['MUTABILITY'])
            self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])

        self.altruism = 1 if self.altruism > 1 else self.altruism
        self.altruism = 0 if self.altruism < 0 else self.altruism

    def __str__(self):

        str = """
        Organism altruism: {}
        Organism velocity: {}
        Organism position: {}
        Organism meals: {}""".format(self.altruism, self.velocity, self.pos, self.meals)

        return str