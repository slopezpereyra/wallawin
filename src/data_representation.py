from matplotlib import pyplot
from matplotlib.patches import Circle, Patch
from wallawin.src.settings import PLOT_SETTINGS
import numpy as np
from os import mkdir


def plot_env(generation, food, step_num, gen_num):
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


def share_or_take_plot(data, name):

    figure2, axis = pyplot.subplots()
    x_axis = np.array(list(data.keys()))
    # Iterate through each step on the data dictionary getting the relevant data.
    y_pop_size = np.array([data[x]['Population Size'] for x in range(0, len(x_axis))])
    abs_selfish_pop = np.array([data[x]['Selfish Population'] for x in range(0, len(x_axis))])

    red_patch = Patch(color='red', label='Selfish population')
    blue_patch = Patch(color='blue', label='Altruistic population')
    pyplot.legend(handles=[red_patch, blue_patch])
    pyplot.xlabel("Generations")
    pyplot.ylabel("Population")
    pyplot.fill_between(x_axis, y_pop_size)
    pyplot.fill_between(x_axis, abs_selfish_pop, facecolor="red")
    pyplot.savefig("data/{}/total_pop_data_{}".format(name, name))

    y_selfish_percentage = np.array([data[x]['Selfish Population Percentage'] for x in range(0, len(x_axis))])
    y_alt_percentage = np.array([data[x]['Altruistic Population Percentage'] for x in range(0, len(x_axis))])

    figure2, axis = pyplot.subplots()
    pyplot.xlabel("Generations")
    pyplot.ylabel("Population Percentage")
    pyplot.plot(x_axis, y_selfish_percentage, color='red')
    pyplot.plot(x_axis, y_alt_percentage, color='blue')
    pyplot.savefig("data/{}/percentual_pop_data_{}".format(name, name))

    y_growth_rate = np.array([data[x]['Population Growth Rate'] for x in range(0, len(x_axis))])

    figure2, axis = pyplot.subplots()
    pyplot.xlabel("Generations")
    pyplot.ylabel("Population Growth Rate")
    pyplot.plot(x_axis, y_growth_rate)
    pyplot.savefig("data/{}/pop_growth_rate_data_{}".format(name, name))


def save_simulation_settings(settings, name):
    f = open('data/{}/settings.txt'.format(name), "w+")
    f.write(str(settings))
