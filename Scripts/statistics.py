import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import pandas as pd


def plotRandom(data, bins = 20):
    hist = data['Score'].plot.hist(bins=20)
    plt.title('Histogram Random Algoritme')
    plt.xlabel('Score: Totale lengte wires')
    plt.ylabel('Frequentie')
    plt.show(hist)


def plotLine(data, name):
    lines = data.plot.line()
    plt.title('Ontwikkeling ' + name)
    plt.xlabel('Iteraties')
    plt.ylabel('Score: Totale lengte wires')
    plt.show(lines)


def plotChip(gates, routeBook, grid):
    # maak een nieuwe plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # definieer assen
    ax.set_xlim([0, 18])
    if grid == "small":
        ax.set_ylim([0, 13])
    else:
        ax.set_ylim([0, 17])
    ax.set_zlim([0, 10])

    # zet ticks op de assem
    ax.set_xticks(np.arange(0, 18, 1))
    if grid == "small":
        ax.set_yticks(np.arange(0, 13, 1))
    else:
        ax.set_yticks(np.arange(0, 17, 1))
    ax.set_zticks(np.arange(0, 10, 1))

    # voeg labels toe
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.set_zlabel('z-axis')

    # voeg alle gates met labels toe
    for gate in gates:
        ax.scatter(gate.x, gate.y, 0)
        ax.text(gate.x, gate.y, 0,
                '%s' % (int(gate.gate)), size=10, zorder=1, color='k')

        # leg wires in plot zoals in het routebook
    for netPoint in routeBook:
        ax.plot([step[0] for step in netPoint.route],
                [step[1] for step in netPoint.route],
                [step[2] for step in netPoint.route])

    plt.show()