from simulator import Simulator
from orgs import AltruisticGen
from random import randint, uniform, choice
from settings import SIM_SETTINGS, PLOT_SETTINGS, Settings
from plotter import alt_plot_epoch_data, plot_step
from math import dist
import copy
import numpy as np


class Altruism (Simulator):
    """Base class for all Simulators centered on altruismtic traits."""

    def __init__(self, settings):
        super().__init__(settings)
        self.alt_pop = [x for x in self.generation if x.altruistic]
        self.self_pop = [x for x in self.generation if not x.altruistic]

    @staticmethod
    def gen_population(size):
        half = int(size / 2)
        alt_pop = [AltruisticGen(altruistic=True, velocity=5) for x in range(0, half)]
        self_pop = [AltruisticGen(altruistic=False, velocity=5) for x in range(0, half)]
        return alt_pop + self_pop

    def fitness_function(self, org, starvation=True):
        """Evaluate fitness of organism org in relation to the amount of meals it ate. Act according to evaluation such
        that no meals produces death, one meal survival and normal chance of reproduction, two meals survival and
        high chance of reproduction."""

        if org.meals == 0 and starvation:
            self.kill(org)
            return

        rep_chance = org.meals * self.settings.rep_factor

        if randint(0, 100) <= rep_chance:
            chiral = copy.deepcopy(org)
            chiral.pos = np.array([uniform(0, SIM_SETTINGS['ENV_SIZE_X']), uniform(0, SIM_SETTINGS['ENV_SIZE_Y'])])
            chiral.age = 0
            if randint(0, 100) <= self.settings.mutation_chance:
                chiral.mutate()
            self.generation.append(chiral)

        if org.age >= self.settings.longevity:
            self.kill(org)

        org.pos = org.start_pos
        org.meals = 0

    def sim_competition(self, organisms):
        """Simulate competition for food in the environment
        given a list of Organism objects by making them mood
        towards the nearest food particle and eat it when at
        feading range distance.."""

        for org in organisms:
            # Check if org has energy, there's food and org can still eat. In any false case, go to next organism.
            if not self.food or org.meals >= 2:
                organisms.remove(org)
                continue

            nearest_food = org.find_food(self.food)
            if dist(org.pos, nearest_food.pos) < self.settings.feading_range:
                org.meals += 1
                self.food.remove(nearest_food)
                del nearest_food
            else:
                org.move_to(nearest_food.pos, effortless=True)

    def evolve(self, starvation=True, static_food_gen=True):
        """Simulate altruistic behavior and evaluate each organism's fitness.
        Then reset organism's meals attribute and regenerate food in the environment."""

        self.altruism()
        # A graph of the previous epoch population data and new epoch population data would be useful here.
        for org in self.generation.copy():
            org.age += 1
            self.fitness_function(org, starvation)

        self.food = self.gen_food(static_food_gen)

    def altruism(self):
        pass

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

            step, epoch = 0, 0
            active_individuals = self.generation.copy()
            epoch_data = {}

            while True:
                step += 1
                if step > SIM_SETTINGS['STEPS'] or len(self.generation) == 0:
                    alt_plot_epoch_data(epoch_data, run)
                    self.generation = self.gen_population(self.settings.pop_size)
                    break

                if PLOT_SETTINGS['PLOT'] is True and step % 5 == 0:
                    plot_step(self.generation, self.food, step, epoch)

                if not active_individuals:
                    self.evolve()
                    epoch += 1
                    active_individuals = self.generation.copy()
                    self.set_epoch_data(epoch, epoch_data)
                    continue

                self.sim_competition(active_individuals)


class ShareWithStarving (Altruism):
    """Altruistic organisms will, if the can survive doing so, share a meal with
    another altruistic organism that failed at getting any on their own.
    Thus they sacrifice reproductive potential in exchange of ensuring
    the survival of another altruistic organisms."""

    def __init__(self, settings):
        super().__init__(settings)

    def altruism(self):
        """Simulates altruistic behavior by making altruistic organisms with
        two meals share one of them with another altruistic organism with zero meals."""

        fit_for_sharing = [org for org in self.alt_pop if org.meals >= 2]
        fit_for_receiving = [org for org in self.alt_pop if org.meals == 0]

        for org in fit_for_sharing:
            if not fit_for_receiving:
                break
            recipient = choice(fit_for_receiving)
            fit_for_receiving.remove(recipient)
            org.share(recipient)


class TakeOrShare (Altruism):

    """Desgined for rep_factor=100"""

    def __init__(self, settings):
        super().__init__(settings)
        self.competitors = []  # Subset of self.generation containing organisms competing for a food particle.
        self.not_compiting = []  # Subset of self.generation containing organisms not competing for a food particle.

    @staticmethod
    def gen_population(size):
        alt_pop = [AltruisticGen(altruistic=False, velocity=5)]
        self_pop = [AltruisticGen(altruistic=True, velocity=5) for x in range(0, size - 1)]
        return alt_pop + self_pop

    def sim_competition(self, organisms):
        """Simulate competition for food in the environment
        given a list of Organism objects by making them chose a random food
        particle and attempt to it it. If the food particle has ben chosen
        by another individual, they will compete for it with three possible situations:

        Both individuals are altruistic:
            Food will be shared. Both survive to the next epoch with low chances of reproduction.
        One individual is altruistic, the other is selfish:
            The selfish individuals takes all the food with high chance of reproduction. Altruistic eats the spoils with
            very low chance of reproduction.
        Both individuals are selfish:
            The individuals will fight for the food with tremendous cost of energy. Very low chance of reproduction."""

        chosen_food = []

        for org in organisms:
            # Chose a random food particle that hasn't been chosen by more than one other organism.
            available_food = [food for food in self.food if chosen_food.count(food) < 2]
            food = choice(available_food)

            # Check if the particle has been chosen by another organism before.
            if food in chosen_food:
                # If that is the case, find the organism that previously chose it and
                # associate it with org as a tuple in the competitors list.
                # Also remove competitor from the list of not compiting organisms.
                competitor = next(x for x in organisms if x.food is food)
                self.competitors.append((org, competitor))
                self.not_compiting.remove(competitor)
            else:
                # If the particle is free for grabs, add the organism to the not compiting list.
                self.not_compiting.append(org)

            org.food = food
            chosen_food.append(org.food)

    def altruism(self):

        for pair in self.competitors:

            if pair[0].altruistic and pair[1].altruistic:
                pair[0].meals, pair[1].meals = 0.5, 0.5
            if not pair[0].altruistic and not pair[1].altruistic:
                pair[0].meals, pair[1].meals = 0.2, 0.2
            else:
                selfish = pair[1] if pair[0].altruistic else pair[0]
                altruistic = pair[1] if selfish is pair[0] else pair[0]
                selfish.meals = 1
                altruistic.meals = 0.2

    def simulate(self, runs=1):

        for run in range(0, runs):

            epoch = 0
            epoch_data = {}

            while True:

                if epoch > SIM_SETTINGS['STEPS'] or len(self.generation) == 0:
                    alt_plot_epoch_data(epoch_data, run)
                    break

                print("EPOCH : ", epoch, " POP ", len(self.generation))
                self.sim_competition(self.generation)
                for org in self.not_compiting:
                    org.meals += 1
                self.evolve(starvation=False, static_food_gen=False)
                self.set_epoch_data(epoch, epoch_data)
                epoch += 1


SETTINGS = Settings(10, 1, rep_factor=100, longevity=2)
ENV = TakeOrShare(SETTINGS)
ENV.simulate()
