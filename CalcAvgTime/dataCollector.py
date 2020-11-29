import os
import pandas as pd
from tabulate import tabulate


def CalculateHPResults():
    print("\nAverage Time for Each Block in HP Test:\n")
    directories = os.listdir('Results/')
    res = []
    for directory in directories:
        entries = os.listdir('Results/{}/'.format(directory))
        row = []
        data = []
        for entry in entries:
            # print('Results/{}/{}'.format(directory, entry))
            file = open('Results/{}/{}'.format(directory, entry), 'r')

            for line in file:
                chuncks = line.strip().split("\t")
                if len(chuncks) > 3:
                    # print(chuncks[2])
                    if chuncks[2].find('time') != -1:
                        times = chuncks[2].strip().split("=")
                        row.append(float(times[1].strip()))
        times = pd.array(row)

        res.append([directory, times.mean()])
        # print("{} is {}".format(directory, times.mean()))
    print(tabulate(res, ['Data Set', 'Average Time'], tablefmt="pretty"))

def CalculateMainResults():
    print("\nAverage Time for Each Block in Main Test:\n")
    directories = os.listdir('Results/')
    res = []
    for directory in directories:
        entries = os.listdir('Results/{}/'.format(directory))
        row = []
        data = []
        for entry in entries:
            # print('Results/{}/{}'.format(directory, entry))
            file = open('Results/{}/{}'.format(directory, entry), 'r')

            for line in file:
                chuncks = line.strip().split("|")
                if len(chuncks) == 3 and chuncks[0].strip().find('example') != -1:
                    # print(chuncks[2])
                    if chuncks[2].find('time') != -1:
                        times = chuncks[2].strip().split("=")
                        row.append(float(times[1].strip()))
        times = pd.array(row)

        res.append([directory, times.mean()])
        # print("{} is {}".format(directory, times.mean()))
    print(tabulate(res, ['Data Set', 'Average Time'], tablefmt="pretty"))

CalculateMainResults()