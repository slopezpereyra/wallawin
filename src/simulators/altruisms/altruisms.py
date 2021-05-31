from wallawin.src.simulators.base_simulator import BaseSimulator
from wallawin.src.settings import SimSettings
from wallawin.src.orgs import AltruisticOrganism


class BaseAltruism(BaseSimulator):

    def __init__(self, sim_settings, org_traits):
        super().__init__(sim_settings, org_traits)

    def evolve(self):
        """Simulate altruistic behavior and evaluate each organism's fitness.
        Then reset organism's meals attribute and regenerate food in the environment."""

        self.altruism()
        for org in self.generation.copy():
            org.age += 1
            self.fitness_function(org)

        self.food = self.gen_food()

    def altruism(self):
        """Base altruism method. The child classes will define their particular altruistic simulations
        by overriding this method."""
        pass


class PredictableAltruism(BaseAltruism):
    """Base class for all Simulators centered on altruismtic traits."""

    def __init__(self, sim_settings, altruistic_org_traits, selfish_org_traits):
        """
        Parameters
        ---------
        sim_settings : SimSettings
            Settings object defining the particular settings of this simulator.
        """
        self.altruistic_org_traits = altruistic_org_traits
        self.selfish_org_traits = selfish_org_traits
        super().__init__(sim_settings)
        self.alt_pop = [x for x in self.generation if x.traits.altruistic]
        self.selfish_pop = [x for x in self.generation if not x.traits.altruistic]

    def gen_population(self, size):
        alt_pop = [AltruisticOrganism(self.env_size, self.altruistic_org_traits) for x in range(0, size - 1)]
        self_pop = [AltruisticOrganism(self.env_size, self.selfish_org_traits)]
        return alt_pop + self_pop

    def get_step_data(self, step):
        """Gather generational data for generation of epoch and
        set it into the epoc_data dictionary (used for plotting).

        Parameters
        ----------
        step : int
            Current epoch (step) of the simulation."""

        speed_values = [x.traits.velocity for x in self.generation]

        pop_size = len(self.generation)
        avg_speed = sum(speed_values) / pop_size if pop_size != 0 else sum(speed_values) / 1
        abs_altruistic_population = len([x for x in self.generation if x.traits.altruistic])
        abs_selfish_population = len([x for x in self.generation if not x.traits.altruistic])
        pop_growth_rate = pop_size - self.data[step - 1]['Population Size'] if step > 0 else 0

        rel_altruistic_population = abs_altruistic_population / pop_size if pop_size != 0 else 0
        rel_selfish_population = abs_selfish_population / pop_size if pop_size != 0 else 0

        if abs_selfish_population != 0:
            altruistic_per_selfish_organisms = abs_altruistic_population / abs_selfish_population
        else:
            altruistic_per_selfish_organisms = 0
        if abs_altruistic_population != 0:
            selfish_per_altruistic_organisms = abs_selfish_population / abs_altruistic_population
        else:
            selfish_per_altruistic_organisms = 1

        self.data[step] = {'Population Size': pop_size, 'Average Speed': avg_speed,
                            'Population Growth Rate': pop_growth_rate,
                            'Altruistic Population': abs_altruistic_population,
                            'Selfish Population': abs_selfish_population,
                            'Altruistic Population Percentage': rel_altruistic_population,
                            'Selfish Population Percentage': rel_selfish_population,
                            'Altruistic organisms per selfish organism': altruistic_per_selfish_organisms,
                            'Selfish organisms per altruistic organisms': selfish_per_altruistic_organisms}


class ContingentAltruism(BaseAltruism):

    def __init__(self, sim_settings, org_traits):
        """
        Parameters
        ---------
        sim_settings : SimSettings
            Settings object defining the particular settings of this simulator.
        """

        # Exception if boolean altruism.
        super().__init__(sim_settings, org_traits)



