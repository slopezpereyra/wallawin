from wallawin.src.simulators.altruisms.altruisms import PredictableAltruism, ContingentAltruism
from wallawin.src.orgs import AltruisticOrganism
from wallawin.src.data_representation import share_or_take_plot
from collections import defaultdict
from random import sample, choice
from wallawin.src.settings import DoveHawkSettings, Traits


class PredictableDoveOrHawk(PredictableAltruism):
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
        """

    def __init__(self, sim_settings, altruistic_org_traits, selfish_org_traits):

        super().__init__(sim_settings, altruistic_org_traits, selfish_org_traits)
        self.chosen_food = defaultdict(list)

    def sim_competition(self):
        """Simulate competition for food by randomly pairing an organism of the generation with a food particle that
        hasn't been chosen by more than one other organism. These creates the possibility that an organism may chose a
        food particle already picked by another, with eventual altruistic/selfish resolutions of the conflict."""

        for org in sample(self.generation, len(self.generation)):
            # Chose a random food particle that hasn't been chosen by more than one other organism.
            available_food = [food for food in self.food if len(self.chosen_food[food]) < 2]
            if not available_food:
                break
            food = choice(available_food)
            self.chosen_food[food].append(org)

    def altruism(self):
        """Simulates altruistic/selfish behavior by determining whether competing pairs should share, take or fight
        for the food, according to the altruistic gen. Three possible cases:

        Both individuals are altruistic:
            Food will be shared. Both survive to the next epoch with low chances of reproduction.
        One individual is altruistic, the other is selfish:
            The selfish individuals takes all the food with high chance of reproduction. Altruistic eats the spoils with
            very low chance of reproduction.
        Both individuals are selfish:
            The individuals will fight for the food with tremendous cost of energy. Very low chance of reproduction."""

        for orgs in self.chosen_food.values():
            if len(orgs) == 0:
                continue
            if len(orgs) == 1:
                orgs[0].meals += 1
                continue

            altruism_a = orgs[0].traits.altruistic
            altruism_b = orgs[1].traits.altruistic

            if altruism_a and altruism_b:
                orgs[0].meals = orgs[1].meals = self.settings.both_altruistic_chance
            elif not altruism_a and not altruism_b:
                orgs[0].meals = orgs[1].meals = self.settings.both_selfish_chance
            else:
                selfish = orgs[1] if altruism_a else orgs[0]
                altruistic = orgs[1] if selfish is orgs[0] else orgs[0]
                selfish.meals = self.settings.alt_and_selfish_chance[1]
                altruistic.meals = self.settings.alt_and_selfish_chance[0]

    def simulate(self, runs=1):
        """Simulate the evolution process, plot and save the data for as many runs as specified.

        Parameters
        ----------
        runs : int
            Number of times the simulation will be run. Set to 1 by default."""

        for run in range(0, runs):

            epoch = 0

            while True:

                if epoch > self.settings.steps or len(self.generation) == 0:
                    share_or_take_plot(self.data, self.settings.simulation_name)
                    break

                self.sim_competition()
                self.evolve()
                self.get_step_data(epoch)
                print("Epoch : ", epoch, " ------- Pop Size : ", len(self.generation),
                      ' ------- ', self.data[epoch]['Selfish Population Percentage'])
                epoch += 1


class ContingentDoveOrHawk(ContingentAltruism):

    def __init__(self, sim_settings, org_traits):
        super().__init__(sim_settings, org_traits)
        self.chosen_food = defaultdict(list)

    def gen_population(self, size):
        pop = [AltruisticOrganism(self.env_size, self.org_traits) for x in range(size)]
        return pop






