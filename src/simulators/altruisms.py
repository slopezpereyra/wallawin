from wallawin.src.base_simulator import BaseSimulator
from wallawin.src.orgs import AltruisticOrganism
from wallawin.src.settings import SIM_SETTINGS, PLOT_SETTINGS, Settings
from wallawin.src.plotter import alt_plot_epoch_data, plot_step

from random import randint, uniform, choice
from math import dist
import copy
import numpy as np


class BaseAltruismSimulator (BaseSimulator):
    """Base class for all Simulators centered on altruismtic traits."""

    def __init__(self, settings):
        """
        Parameters
        ---------
        settings : Settings
            Settings object defining the particular settings of this simulator.
        """
        super().__init__(settings)
        self.alt_pop = [x for x in self.generation if x.altruistic]
        self.self_pop = [x for x in self.generation if not x.altruistic]

    @staticmethod
    def gen_population(size):
        """
        Method that generates an initial set of organisms, halved by altruistic and selfish individuals.

        Parameters
        ----------
        size : int
            The number of organisms of the starting population.
        """
        half = int(size / 2)
        alt_pop = [AltruisticOrganism(altruistic=True, velocity=5) for x in range(0, half)]
        self_pop = [AltruisticOrganism(altruistic=False, velocity=5) for x in range(0, half)]
        return alt_pop + self_pop

    def fitness_function(self, org):
        """Evaluate fitness of organism org in relation to the amount of meals it ate.
        Act according to evaluation such that no meals produces death, one meal survival
        with  normal chance of reproduction, two meals survival with high chance of reproduction.
        If starvation is set to false on the settings, organism will survive even when not eating
        any food particle.

        Parameters
        ----------
        org : Organism
            The organism whose fitness is to be evaluated.
        """

        if org.meals == 0 and self.settings.starvation:
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
        feading range distance.

        Parameters
        ----------
        organisms : list
            List of organisms to simulate the competition with."""

        for org in organisms:
            # Check if there's food and org can still eat. In any false case, go to next organism.
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

    def evolve(self):
        """Simulate altruistic behavior and evaluate each organism's fitness.
        Then reset organism's meals attribute and regenerate food in the environment."""

        self.altruism()
        # A graph of the previous epoch population data and new epoch population data would be useful here.
        for org in self.generation.copy():
            org.age += 1
            self.fitness_function(org)

        self.food = self.gen_food()

    def altruism(self):
        """Base altruism method. The child classes will define their particular altruistic simulations
        by overriding this method."""
        pass

    def set_epoch_data(self, epoch, epoch_data):
        """Gather generational data for generation of epoch and
        set it into the epoc_data dictionary (used for plotting).

        Parameters
        ----------
        epoch : int
            Current epoch (step) of the simulation.
        epoch_data : dictionary
            A dictionary containing relevant data from this epoch."""

        speed_values = [x.velocity for x in self.generation]

        pop_size = len(self.generation)
        avg_speed = sum(speed_values) / pop_size if pop_size != 0 else sum(speed_values) / 1
        abs_altruistic_population = len([x for x in self.generation if x.altruistic])
        abs_selfish_population = len([x for x in self.generation if not x.altruistic])
        epoch_data[epoch] = [pop_size, avg_speed, abs_altruistic_population, abs_selfish_population]

    def simulate(self, runs=1):
        """Simulate the evolution process, plot and save the data for as many runs
        as specified.

        Parameters
        ----------
        runs : int
            Number of times the simulation will be run. Set to 1 by default."""

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


class SharingSimulator (BaseAltruismSimulator):
    """Simulator in which altruistic organisms will, if the can survive doing so,
    share a meal with another altruistic organism that failed at getting any on their own.
    Thus they sacrifice reproductive potential in exchange of ensuring
    the survival of another altruistic organisms. Selfish organisms will always keep
    their food for themselves."""

    def __init__(self, settings):
        super().__init__(settings)

    def altruism(self):
        """Simulates altruistic behavior by making altruistic organisms with
        two meals share one of them with another altruistic organism with zero meals
        if possible."""

        fit_for_sharing = [org for org in self.alt_pop if org.meals >= 2]
        fit_for_receiving = [org for org in self.alt_pop if org.meals == 0]

        for org in fit_for_sharing:
            if not fit_for_receiving:
                break
            recipient = choice(fit_for_receiving)
            fit_for_receiving.remove(recipient)
            org.share(recipient)


class TakeOrShareSimulator (BaseAltruismSimulator):

    """Simulator in which all organisms are garanteed to find a meal. Same meal may be found by
    two different organisms. If that is the case, the issue will be solved according to whether
    the encountering organisms are both altruistic, both selfish or one of each.

    CASES :
        BOTH ALTRUISTIC : The meal will be shared, ensuring certain reproductive potential for both.
        BOT SELFISH : They'll fight for the food, wasting a lot of energy. Low reproductive potential for both.
        ONE OF EACH : The selfish organism takes the food. High reproductive potential for him, low for his
                    altruistic counterpart.

    SPECS :
        This simulator is desgined for a rep_factor of 100.

    Attributes
    ----------
    both_altruistic_chance : float
        A float between 0 and 1. Represents the reproductive potential of altruistic organisms that
        meet and share their food. Set to 0.5 by default.
    both_selfish_chance : float
        A float between 0 and 1. Represents the reproductive potential of selfish organisms that
        meet and share their food. Set to 0.2 by default.
    alt_and_selfish_chance : list
        A list of two floats between 0 and 1. The first represents the reproductive potential
         of an altruistic organism that meets a selfish one. Set to 0.2 by default.
        The second one represents the reproductive potential of a selfish organisms
        that meets an altruistic one. Set to 0.8 by default.
    competitors : list
        Subset of self.generation containing organisms competing for a food particle.
    not_competing : list
        Subset of self.generation containing organisms not competing for a food particle.
        """

    def __init__(self, settings, both_altruistic_chance = 0.5, both_selfish_chance = 0.2,
                         alt_and_selfish_chance = [0.2, 0.8]):
        super().__init__(settings)
        self.both_altruistic_chance = both_altruistic_chance
        self.both_selfish_chance = both_selfish_chance
        self.alt_and_selfish_chance = alt_and_selfish_chance
        self.competitors = []  # Subset of self.generation containing organisms competing for a food particle.
        self.not_compiting = []  # Subset of self.generation containing organisms not competing for a food particle.

    @staticmethod
    def gen_population(size):
        alt_pop = [AltruisticOrganism(altruistic=False, velocity=5)]
        self_pop = [AltruisticOrganism(altruistic=True, velocity=5) for x in range(0, size - 1)]
        return alt_pop + self_pop

    def sim_competition(self, organisms):
        """Simulate competition for food in the environment
        given a list of Organism objects by making them chose a random food
        particle and attempt to eat it. If the food particle has also been chosen
        by another individual, they will compete for it with three possible cases:

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
        """Simulates altruistic behavior by determining whether competing pairs
        should share, take or fight for the food, according to the altruistic
        behavior of the involved organisms."""

        for pair in self.competitors:

            if pair[0].altruistic and pair[1].altruistic:
                pair[0].meals = pair[1].meals = self.both_altruistic_chance
            if not pair[0].altruistic and not pair[1].altruistic:
                pair[0].meals = pair[1].meals = self.both_selfish_chance
            else:
                selfish = pair[1] if pair[0].altruistic else pair[0]
                altruistic = pair[1] if selfish is pair[0] else pair[0]
                selfish.meals = self.alt_and_selfish_chance[1]
                altruistic.meals = self.alt_and_selfish_chance[0]

    def simulate(self, runs=1):
        """Simulate the evolution process, plot and save the data for as many runs
                as specified.

                Parameters
                ----------
                runs : int
                    Number of times the simulation will be run. Set to 1 by default."""

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
                self.evolve()
                self.set_epoch_data(epoch, epoch_data)
                epoch += 1


SETTINGS = Settings(10, 1, rep_factor=100, longevity=2, starvation=False, static_food_generation=False)
ENV = TakeOrShareSimulator(SETTINGS)
ENV.simulate()
