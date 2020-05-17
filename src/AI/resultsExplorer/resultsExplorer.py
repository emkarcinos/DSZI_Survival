"""
A small script to help you analyze the output logs from GA algorithm.
It shows you best and worst population with all values.
Specify the input file as an exec parameter.
"""

import sys
from ast import literal_eval
import matplotlib.pyplot as plt
import numpy


def fitnessPlot(pop):
    """
    Draw a fitness plot and write it to a file

    :param pop: Population array with fitness
    """
    fig, ax = plt.subplots()
    ax.plot([i[4] for i in pop])
    ax.set_title("Best fitness by generation")
    ax.set_ylabel("Fitness")
    ax.set_xlabel("Generation")
    fig.legend()
    fig.show()
    fig.savefig("fitnessPlot")
    print("Figure saved to file.")


def printBestWorstGenes(pop):
    """
    Print info about best and worst specimen.

    :param pop: Population array with fitness
    """
    fitnesses = [i[4] for i in pop]
    bestIdxs = (numpy.where(fitnesses == numpy.max(fitnesses)))[0]

    print("Best Fitness:", max(fitnesses))
    for idx in bestIdxs:
        print("Affinities: food={}, water={}, rest={}, walking={}".format(pop[idx][0], pop[idx][1],
                                                                          pop[idx][2], pop[idx][3]))

    worstIdxs = (numpy.where(fitnesses == numpy.min(fitnesses)))[0]

    print("Worst Fitness:", min(fitnesses))
    for idx in worstIdxs:
        print("Affinities: food={}, water={}, rest={}, walking={}".format(pop[idx][0], pop[idx][1],
                                                                          pop[idx][2], pop[idx][3]))


if len(sys.argv) < 2:
    print("No file specified.")
else:
    with open(sys.argv[1], "r") as file:
        if file.readline() != "=HEADER=GA=\n":
            print("Invalid header. Incorrect file or missing header?")
        else:
            # Load data into memory
            pop = []
            for line in file:
                pop.append(literal_eval(line))

            fitnessPlot(pop)
            printBestWorstGenes(pop)
