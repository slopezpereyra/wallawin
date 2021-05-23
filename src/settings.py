
"""Stores global settings for the simulation."""

SIM_SETTINGS = {'ENV_SIZE_X': 100,
                'ENV_SIZE_Y': 100,
                'STEPS': 100}

PLOT_SETTINGS = {'PLOT': False,
                 'X_MIN': 0.0,
                 'X_MAX': 100.0,
                 'Y_MIN': 0.0,
                 'Y_MAX': 100.0}

ENV_SETTINGS = {'POP_SIZE'}


class Settings:

    def __init__(self, pop_size, abundance, mutation_chance=10, mutability=1.2, feading_range=10, longevity=400000,
                 risk=0, rep_factor=40, starvation=True, static_food_generation=True):
        self.pop_size = pop_size
        self.abundance = abundance
        self.mutation_chance = mutation_chance
        self.mutability = mutability
        self.feading_range = feading_range
        self.longevity = longevity
        self.risk = risk
        self.rep_factor = rep_factor
        self.starvation = starvation
        self.static_food_generation = static_food_generation


