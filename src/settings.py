"""Stores global settings for the simulation."""

PLOT_SETTINGS = {'PLOT': False,
                 'X_MIN': 0.0,
                 'X_MAX': 100.0,
                 'Y_MIN': 0.0,
                 'Y_MAX': 100.0}


class SimSettings:
    """
    Base class for Simulator Settings. All configurations related to the simulation are stablished on an instance
    of this object.

    Attributes
    ----------
    steps : int
        How many steps will the simulation last. Each step is a particular instance of the simulation.
    pop_size : int
        Number of the initial population.
    abundance : float
        A factor that determines how much food it will be in the environment in relation to the population size.
        A factor of 1 specifies same amount of food as amount of individuals; a factor of 2, twice; a factor of 0.5,
        a half, etc.
    runs : int
        How many simulations will be run with the configured Simulator.
    mutation_chance : float
        Float between 0 and 100 representing the chance an organism has of presenting a mutation
        on birth.
    mutability : float
        Float that represents the amount of absolute change a trait can present on mutation.
    feading_range : float
        Relevant on simulations with movement. Distance the organism must be from the food to be able to eat it.
    base_longevity : int
        Default longevity of the organisms of the initial population. Longevity determines how many reproductive
        cycles the'll live.
    risk : float
        Chance of random death for an organism. Represents the danger level of the environment.
    rep_factor : float
        A factor that determines an organism's chance of reproducing in function of the amount of meals it ate
        so that chance = meal_amount * rep_factor.
    starvation : bool
        If true organisms that fail at getting any food die.
    static_food_generation : bool
        If true, the same amount of food is generated after each reproductive cycle. If false, the amount of food
        generated is related to the size of the population by the abundance factor.
    env_size_x : int
        Horizontal length of the 2D space in which the simulation is carried. Only relevant in simulations
        that involve movement.
    env_size_y : int
        Vertical length of the 2D space in which the simulation is carried. Only relevant in simulations
        that involve movement.
    """

    def __init__(self, steps, pop_size, abundance, rep_factor, simulation_name, runs=1, mutation_chance=10,
                 mutability=1.2,
                 feading_range=10,
                 base_longevity=400000, risk=0, starvation=True, static_food_generation=True,
                 env_size_x=100, env_size_y=100):
        self.steps = steps
        self.pop_size = pop_size
        self.abundance = abundance
        self.runs = runs
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
        self.simulation_name = simulation_name

    def __str__(self):

        string = """
        SIMULATION SETTINGS
         
        STEPS : {}
        INITIAL POPULATION : {}
        RUNS : {}
        ENVIRONMENT SIZE {}x{}
        
        ECOLOGICAL/ENVIRONMENTAL SETTINGS
        
        ABUNDANCE : {}
        BASE LONGEVITY : {}
        STATIC FOOD GENERATION : {}
        STARVATION : {}        
        RISK : {}

        REPRODUCTIVE SETTINGS 
        
        REPRODUCTION FACTOR : {}
        MUTATION CHANCE : {}
        MUTABILITY : {}
        
        OTHERS
        
        FEADING RANGE : {}
        """.format(self.steps, self.pop_size, self.runs, self.env_size_x, self.env_size_y, self.abundance,
                   self.base_longevity, self.static_food_generation, self.starvation, self.risk, self.rep_factor,
                   self.mutation_chance, self.mutability, self.feading_range)

        return string


class DoveHawkSettings(SimSettings):
    """
        Specific class for TakeOrShare simulation settings.

        Attributes
        ----------
        steps : int
            How many steps will the simulation last. Each step is a particular instance of the simulation.
        pop_size : int
            Number of the initial population.
        abundance : float
            A factor that determines how much food it will be in the environment in relation to the population size.
            A factor of 1 specifies same amount of food as amount of individuals; a factor of 2, twice; a factor of 0.5,
            a half, etc.
        runs : int
            How many simulations will be run with the configured Simulator.
        mutation_chance : float
            Float between 0 and 100 representing the chance an organism has of presenting a mutation
            on birth.
        mutability : float
            Float that represents the amount of absolute change a trait can present on mutation.
        feading_range : float
            Relevant on simulations with movement. Distance the organism must be from the food to be able to eat it.
        base_longevity : int
            Default longevity of the organisms of the initial population. Longevity determines how many reproductive
            cycles the'll live.
        risk : float
            Chance of random death for an organism. Represents the danger level of the environment.
        rep_factor : float
            A factor that determines an organism's chance of reproducing in function of the amount of meals it ate
            so that chance = meal_amount * rep_factor.
        starvation : bool
            If true organisms that fail at getting any food die.
        static_food_generation : bool
            If true, the same amount of food is generated after each reproductive cycle. If false, the amount of food
            generated is related to the size of the population by the abundance factor.
        env_size_x : int
            Horizontal length of the 2D space in which the simulation is carried. Only relevant in simulations
            that involve movement.
        env_size_y : int
            Vertical length of the 2D space in which the simulation is carried. Only relevant in simulations
            that involve movement.
        both_altruistic_chance : float
            Float between 0 and 1 representing the chance competing organisms have of reproducing if both are
            altruistic.
        both_selfish_chance : float
            Float between 0 and 1 representing the chance competing organisms have of reproducing if both are
            selfish.
        alt_and_selfish_chance : list
            A list l containing two floats such that, when an altruistic organism competes with a selfish one,
            l[0] is the chance of reproduction of the first and l[1] that of the second.
        """

    def __init__(self, steps, pop_size, abundance, rep_factor, simulation_name, runs=1, mutation_chance=10,
                 mutability=1.2,
                 feading_range=10,
                 base_longevity=400000, risk=0, starvation=True, static_food_generation=True,
                 env_size_x=100, env_size_y=100, both_altruistic_chance=0.5, both_selfish_chance=0.2,
                 alt_and_selfish_chance=[0.2, 0.8]):
        super().__init__(steps, pop_size, abundance, rep_factor, simulation_name, runs, mutation_chance, mutability,
                         feading_range, base_longevity, risk, starvation, static_food_generation,
                         env_size_x, env_size_y)
        self.both_altruistic_chance = both_altruistic_chance
        self.both_selfish_chance = both_selfish_chance
        self.alt_and_selfish_chance = alt_and_selfish_chance

    def __str__(self):

        string = """
                SIMULATION SETTINGS

                STEPS : {}
                INITIAL POPULATION : {}
                RUNS : {}
                ENVIRONMENT SIZE {}x{}

                ECOLOGICAL/ENVIRONMENTAL SETTINGS

                ABUNDANCE : {}
                BASE LONGEVITY : {}
                STATIC FOOD GENERATION : {}
                STARVATION : {}        
                RISK : {}

                REPRODUCTIVE SETTINGS 

                REPRODUCTION FACTOR : {}
                MUTATION CHANCE : {}
                MUTABILITY : {}
                
                REPRODUCTION CHANCES:
                
                BOTH ALTRUISTIC : {}
                BOTH SELFISH : {}
                ALTRUISTIC THAT MEETS SELFISH : {}
                SELFISH THAT MEETS ALTRUISTIC : {}

                OTHERS

                FEADING RANGE : {}
                """.format(self.steps, self.pop_size, self.runs, self.env_size_x, self.env_size_y, self.abundance,
                           self.base_longevity, self.static_food_generation, self.starvation, self.risk,
                           self.rep_factor,
                           self.mutation_chance, self.mutability, self.both_altruistic_chance,
                           self.both_selfish_chance, self.alt_and_selfish_chance[0],
                           self.alt_and_selfish_chance[1], self.feading_range)

        return string


class Traits:
    """An object holding the values of the evolutionary traits of an organism.

    Attributes
    ----------
    longevity : int
        Longevity of the organism.
    altruistic : bool
        Determines if organism is altruistic or not.
    velocity : float
        Distance covered by the individual in a single evolutionary step.
        Only relevant in simulations that involve movement.
    energy : float
         Amount of energy available to spend in search for food each step. Only
        relevant in simulations involving movement.
    energy_release : float
        A factor determining how quickly the energy is released.
        Energy release is always proportionally equivalent to velocity.
        Only relevant in simulations involving movement.
    """

    def __init__(self, altruistic, longevity, velocity=5, energy=10, energy_release=0.1):
        self.longevity = longevity
        self.velocity = velocity
        self.energy = energy
        self.energy_release = energy_release
        self.altruistic = altruistic


TEST = DoveHawkSettings(100, 10, 2, 100, simulation_name="test_1", base_longevity=33, static_food_generation=True)
