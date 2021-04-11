"""Organisms' traits and behavior."""

from random import uniform, getrandbits
from math import dist
import numpy as np
from global_settings import ENV_SETTINGS


class Organism:
    """Defines an organism object capable of interacting with an environment,
    eating, reproducing and dying."""

    def __init__(self, velocity=uniform(1, 2)):
        self.altruistic = bool(getrandbits(1))
        self.velocity = velocity
        self.pos = np.array([uniform(0, ENV_SETTINGS['ENV_SIZE_X']), uniform(0, ENV_SETTINGS['ENV_SIZE_Y'])])
        self.start_pos = self.pos
        self.meals = 0

    def update_pos(self, target_pos):
        """Move the organism towards the target_pos."""

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

    def mutate(self):
        """Mutate the altruism, velocity or both depending on a random choice."""

        a = range(0, 1)
        if a == 0:
            self.altruism *= uniform(1, ENV_SETTINGS['MUTABILITY'])
        elif a == 1:
            self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])
        #else:
        #    self.altruism *= uniform(1, ENV_SETTINGS['MUTABILITY'])
        #    self.velocity *= uniform(1, ENV_SETTINGS['MUTABILITY'])

    def __str__(self):

        str = """
        Organism fitness: {}
        Organism altruism: {}
        Organism velocity: {}
        Organism position: {}
        Organism meals: {}""".format(self.fitness, self.altruism, self.velocity, self.pos, self.meals)

        return str
