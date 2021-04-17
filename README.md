# Wallawin

## What is it?

Wallawin is an evolution simulation program with an emphasis on behavioral traits. In other words, it simulates the action of natural selection over behavioral traits, such as altruism or selfishness, across a series of generations.

## State of development

Basic mechanics of evolutionary simulation are completed. Only currently developed model is based on altruistic and not altruistic individuals.

## How does it work

Wallawin simulates the process of evolution in an abstract space, an Environment, moving through an abstract time unit, a Step. A Step is simply a particular instance of the simulation. Organisms move, reproduce, act and live from one step to another.

On the Environment individuals compete for food and survival, reproduce and die. Simulations on different type of environments correspond to simulations under different rules. The general principle across different forms of simulation is that the chance of reproduction of an individual depends on their success at finding food, and that if an individual fails at finding any food at all it dies.

## The environment of the altruistic gen

In this environment an altruistic gen exists in the population, making them *potentially* altruistic. 

Altruistic individuals will share their food with other altruistic individuals that failed at finding food on their own. They only share if they do not compromise their own survival in doing so. The altruistic organism thus trades a high chance of self reproduction by a slight chance of reproduction and the survival of another altruistic individual, which not only has a slight chance of reproduction itself but may now show reciprocity in the future. 

Not altruistic, or selfish, individuals will never share their extra food with other organisms, and will invest of it in their own reproductive potential directly.

## Example

Here we see the simulation of the evolutionary process with selfish (red) and green (altruistic) individuals in an environment of very abundant resources
in the course of around 30 generations (1000 steps).
In this environment the altruistic popoulation shows a constant growth and surpasses the selfish one around the 15th generation.
The selfish population grows until the 20th generation, when it begins to fall.
The speed of the individuals plays no part, probably as a consequence of the extreme abundance of food.



![Alt Text](https://tenor.com/view/gif-21204878)


![Evolutionary Data](https://i.ibb.co/pWwXMgm/data.png)


