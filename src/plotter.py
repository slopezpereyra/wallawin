from matplotlib import pyplot
from matplotlib.patches import Circle, Patch
from wallawin.src.settings import PLOT_SETTINGS
import numpy as np
import os

def plot_step(generation, food, step_num, gen_num):
    """Function that plots a particular step of the evolutionary simulation."""

    figure, axis = pyplot.subplots()
    figure.set_size_inches(9.6, 5.4)

    pyplot.xlim(PLOT_SETTINGS['X_MIN'], PLOT_SETTINGS['X_MAX'])
    pyplot.ylim(PLOT_SETTINGS['Y_MIN'], PLOT_SETTINGS['Y_MAX'])

    for org in generation:
        altruistic_color = (0, 1, 0) if org.altruistic else (1, 0, 0)
        org_circle = Circle(org.pos, 0.75, edgecolor=altruistic_color, facecolor=altruistic_color, zorder=8)
        edge = Circle(org.pos, 0.05, facecolor='None', edgecolor=altruistic_color, zorder=8)
        pyplot.text(org.pos[0], org.pos[1] + 1, "m=" + str(org.meals))
        pyplot.text(org.pos[0], org.pos[1] - 1, "e=" + str(int(org.energy)))
        axis.add_patch(org_circle)
        axis.add_patch(edge)
    for food in food:
        food_circle = Circle(food.pos, 0.65, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
        axis.add_patch(food_circle)

    axis.set_aspect('equal')
    frame = pyplot.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])

    pyplot.figtext(0.025, 0.95, r'GENERATION: ' + str(gen_num))
    pyplot.figtext(0.025, 0.90, r'T_STEP: ' + str(step_num))

    pyplot.savefig('step {}.png'.format(step_num), dpi=100)


def alt_plot_epoch_data(data, run):

    figure2, axis = pyplot.subplots()

    x_axis = np.array(list(data.keys()))
    print(data)
    print(data[0][0])
    # Iterate through each step on the data dictionary getting the relevant data.
    y_pop_size = np.array([data[x][0] for x in range(0, len(x_axis))])
    abs_selfish_pop = np.array([data[x][3] for x in range(0, len(x_axis))])

    red_patch = Patch(color='red', label='Selfish population')
    blue_patch = Patch(color='blue', label='Altruistic population')
    pyplot.legend(handles=[red_patch, blue_patch])
    pyplot.xlabel("Generations")
    pyplot.ylabel("Population")
    pyplot.fill_between(x_axis, y_pop_size)
    pyplot.fill_between(x_axis, abs_selfish_pop, facecolor="red")
    pyplot.savefig("data_{}".format(run))
