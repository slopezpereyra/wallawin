# Wallawin

## What is it?

Wallawin is an evolution simulation program with an emphasis on behavioral traits. In other words, it simulates the action of natural selection over behavioral traits, such as altruism or selfishness, across a series of generations.

## State of development

Basic mechanics of evolutionary simulation are completed. Only currently developed model is based on altruistic and not altruistic individuals.

## How does it work

Wallawin simulates the process of evolution in an abstract space named Environment. Moving through an abstract time unit, a Step, wich signifies a particular instance of the simulation, organisms move, reproduce, act and evolve.

Simulations on different type of environments correspond to simulations under different rules. The general principle across different forms of simulation is that the chance of reproduction of an individual depends on their success at finding food, and that if an individual fails at finding any food at all it dies.

## Altruism Simulations

Altruism simulations are those in which organisms are altruistic or selfish, depending on the allele of a gen.

### Sharing simulation

Altruistic individuals will share their food with other altruistic individuals that failed at finding food on their own, so long as they do not compromise their own survival in doing so. The altruistic organism thus trades a high chance of self reproduction by a slight chance of reproduction and the survival of another altruistic individual, which not only has a slight chance of reproduction itself but may now show reciprocity in the future. 

Selfish individuals will never share their extra food with other organisms, and will invest it on their own reproductive potential directly.

### Share or take simulation

All organisms are garanteed to find a meal, but a single meal may be found by two of them. If this is the case, they'll decide how to resolve this problem based on both of their altruistic alleles. If two altruistic individuals meet, they'll split the meal ensuring an medium chance of reproducing for each of them. If both are selfish, they'll fight for the meal and have a low chance of reproducing as a consequence of energy waste. If a selfish organism meets an altruistic one, it will take the food for himself ensuring his own reproduction, while his altruistic counterpart will have a low chance of reproducing.

## Some example

Here we see a *Sharing Simulation* with selfish (red) and altruistic (green) individuals in an environment of very abundant resources in the course of around 30 generations (1000 steps). In this case the altruistic popoulation shows a constant growth and surpasses the selfish one around the 15th generation. The selfish population grows until the 20th generation, when it begins to fall. The speed of the individuals plays no part, probably as a consequence of the extreme abundance of food.



![Alt Text](https://media.giphy.com/media/5AW6l3xZx2gw71l4Rw/giphy.gif)


![Evolutionary Data](https://i.ibb.co/pWwXMgm/data.png)

The next is a *Share or take simulation* starting with 9 altruistic and 1 selfish individuals. We see the total population grow with a somewhat constant proportion of altruistic/selfish organisms until around generation 30, where selfish organisms succeed greatly and drive altruistic ones to extintion. This results in a tremendous drop of the total population and eventual extinction of the species around the 90th generation. A case of success of an evolutionary trait at the cost of the good of the species.

![Evolutionary Data](https://i.ibb.co/qpCnC9C/data-0.png)

