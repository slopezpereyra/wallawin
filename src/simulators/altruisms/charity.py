from altruisms import PredictableAltruism
from random import choice
from math import dist
from wallawin.src.data_representation import plot_env, share_or_take_plot, PLOT_SETTINGS


class Charity(PredictableAltruism):
    """Simulator in which altruistic organisms will, if the can survive doing so,
    share a meal with another altruistic organism that failed at getting any on their own.
    Thus they sacrifice reproductive potential in exchange of ensuring
    the survival of another altruistic organisms. Selfish organisms will always keep
    their food for themselves."""

    def __init__(self, sim_settings, alt_org_traits, selfish_org_traits):
        super().__init__(sim_settings, alt_org_traits, selfish_org_traits)

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

    def simulate(self):
        """Simulate the evolution process, plot and save the data for as many runs
        as specified."""

        for run in range(0, self.settings.runs):

            step, epoch = 0, 0
            active_individuals = self.generation.copy()
            epoch_data = {}

            while True:
                step += 1
                if step > self.settings.steps or len(self.generation) == 0:
                    share_or_take_plot(epoch_data, run)
                    self.generation = self.gen_population(self.settings.pop_size) # ?
                    break

                if PLOT_SETTINGS['PLOT'] is True and step % 5 == 0:
                    plot_env(self.generation, self.food, step, epoch)

                if not active_individuals:
                    self.evolve()
                    epoch += 1
                    active_individuals = self.generation.copy()
                    self.get_step_data(epoch)
                    continue

                self.sim_competition(active_individuals)