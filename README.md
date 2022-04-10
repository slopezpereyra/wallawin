# Wallawin

## What is it?

Wallawin is an evolution simulation program with an emphasis on behavioral traits. It simulates the action of natural selection on behavioral traits across a series of generations. Its goal is to provide a computational model for hypothesis testing in evolutionary psychology.

## How does it work

Wallawin simulates the process of evolution in an abstract space. Moving through an abstract time units that signify an individual instance of the evolutionary process, organisms live, reproduce, act and evolve.

Simulations on different type of simulators correspond to simulations under different rules. The general principle across different forms of simulation is that the chance of reproduction of an individual depends on the amount of food they were succesful to get, though this is only a representation of their abstract adaptability and can be flexibly adjusted to fit other models.

## Altruism Simulations

Altruism simulations are those in which organisms are altruistic or selfish, depending on the allele of a gen. There are currently two types of altruism simulations.

### Charity simulation

Altruistic individuals will share their food with other altruistic individuals that failed at finding food on their own, so long as they do not compromise their own survival in doing so. The altruistic organism thus trades a high chance of reproduction by a slight one plus the survival of another altruistic individual, which not only has a slight chance of reproduction itself but may now show reciprocity in the future. 

Selfish individuals will never share their extra food with other organisms, and will always invest it on their own reproductive potential directly.

### Dove Hawk simulation

All organisms are garanteed to find a meal, but a single meal may be found by two of them. If this is the case, they'll decide how to resolve this problem based on both of their altruistic alleles. If two altruistic individuals encounter each other, they'll split the meal ensuring a medium chance of reproduction for each of them. If both are selfish, they'll fight for the meal and have a low chance of reproduction as a consequence of energy waste. If a selfish organism meets an altruistic one, the first will take the food for himself and ensure his own reproduction, while his altruistic counterpart will have low chances of reproductive success.

## Examples

### Charity Simulation

Here we see a *Charity simulation*. Selfish (red) and altruistic (green) individuals 
compete for food in an environment of very abundant resources in the course of around 
30 generations (1000 steps). 

In this case the altruistic popoulation shows a constant growth and surpasses the selfish one 
around the 15th generation. The selfish population grows until the 20th generation, when it begins to fall.
The speed of the individuals plays no part, probably as a consequence of the extreme abundance of food.


![Alt Text](https://media.giphy.com/media/5AW6l3xZx2gw71l4Rw/giphy.gif)


![Evolutionary Data](https://i.ibb.co/pWwXMgm/data.png)

### Hardy-Weinberg Equilibrium in Dove Hawk Simulations

The next are two examples of Dove Hawk Simulations in which a state of equilibrium is reached.
The Hardy-Weinberg principle states that a constant frequence of an allele will remain in a population
not affected by other evolutionary influences. It is interesting to study what the equilibrium is for
altruistic/selfish alleles in different type of environments or with different species.

#### Simulation A

This simulation was carried in a highly abundant environment (**abundance factor=100**) 
with an initial population of 9 altruistic and 1 selfish individuals. All organisms have a longevity
of two generations. The selfish organisms of the species have 20% chances of reproducing after competing 
for a food particle with another selfish individual; meeting altruistic individuals a 50% chance.
On the case of an altruistic competing with a selfish individual, 20% and 80% reproduction chances
are given respectively.

We see the population quickly grow beyond the environment's carrying capacity and reach a constant number
of around a thousand individuals, in a clear case of **logarithmic population growth**.

An equilibrium of around 9/10 selfish individuals is reached and mantained around the 60th generation.


![Evolutionary Data](https://i.ibb.co/YXWWsB7/total-pop-data-test-6.png)


#### Simulation B

All settings are the same as in Simulation A, except now selfish individuals have 0% chances of 
mating after competing for food with another selfish individual. Now the equilibrium is reached at
a proportion of around 40% selfish individuals in the population with a stable total population of 
around 1500 indidivuals.

![Evolutionary Data](https://i.ibb.co/NKx563S/total-pop-data-test-8.png)

By comparing the species of the Simulation A with the one of Simulation B we can see that higher risk
implied in selfish behavior logically leads to an inferior amount of selfish individuals, which in turns
seems to, in this particular case, benefit the entire species by reducing the chance of unfavourable
mates and yielding a greater total population.

## On work features

- Develop reciprocity in the altruism simulations. Organisms that cooperate in one instance should remember this and prioritize cooperation with each other in future steps of the simulation.
- Longevity of individuals is currently a setting, while it should be an evolutionary trait in at least certain simulations.
- A complex simulator that combines both *Dove Hawk* and *Charity* simulations will be developed. This simulator will include both behavioral processes: the possibility of altruistic organisms to share their food with other starving altruistic organisms, and the chance of a single meal to be found by different kind of organisms, with the eventual resolution of the conflict based on the allele of their altruistic gen.
- Concrete, ready-to-go Setting objects must be defined to establish the predetermined configuration of different kind of simulators.
- Other behavioral traits must be simulated both on their own simulators as well as mixed in the already existing ones. Some of them are agressivness, kin selection, infanticide or, in a complex level, different degrees of promiscuity. The list is not limited to these.
