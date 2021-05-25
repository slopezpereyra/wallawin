
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


class SimSettings:

    def __init__(self, steps, pop_size, abundance, mutation_chance=10, mutability=1.2, feading_range=10, base_longevity=400000,
                 risk=0, rep_factor=40, starvation=True, static_food_generation=True, env_size_x=100, env_size_y=100):
        self.steps = steps
        self.pop_size = pop_size
        self.abundance = abundance
        self.mutation_chance = mutation_chance
        self.mutability = mutability
        self.feading_range = feading_range
        self.base_longevity = base_longevity
        self.risk = risk
        self.rep_factor = rep_factor
        self.starvation = starvation
        self.static_food_generation = static_food_generation
        self.env_size_x = env_size_x
        self.env_size_y = env_size_y


class TakeOrShareSettings(SimSettings):

    def __init__(self, steps, pop_size, abundance, both_altruistic_chance, both_selfish_chance, alt_and_selfish_chance,
                 mutation_chance=10, mutability=1.2, feading_range=10, base_longevity=400000, risk=0, rep_factor=40,
                 starvation=True, static_food_generation=True, env_size_x=100, env_size_y=100):

        super().__init__(steps, pop_size, abundance, mutation_chance, mutability, feading_range, base_longevity,
                         risk, rep_factor, starvation, static_food_generation, env_size_x, env_size_y)
        self.both_altruistic_chance = both_altruistic_chance
        self.both_selfish_chance = both_selfish_chance
        self.alt_and_selfish_chance = alt_and_selfish_chance


class Traits:

    def __init__(self, longevity, altruistic, velocity=5, energy=10, energy_release=0.1):
        self.longevity = longevity
        self.velocity = velocity
        self.energy = energy
        self.energy_release = energy_release
        self.altruistic = altruistic


