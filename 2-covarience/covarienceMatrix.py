"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #2 - Covarience matrix
By Jesse Braaksma
13/05/2021
"""

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt


dataFilePath = "2-covarience/data.csv"
dataDF = pd.read_csv(dataFilePath, names=['x', 'y', 'z'], header=0)


def cov(x, y):
    ''' Calculate the covariance between x and y, where x and y are both a list of numbers '''

    xMean, yMean = x.mean(), y.mean()
    cov = np.sum((x - xMean) * (y - yMean)) / len(x)
    return cov

# Create the covariance matrix based on the size of the data, using the cov function
numberOfVariables = len(dataDF.columns) 
covMatrix = np.empty([numberOfVariables, numberOfVariables])

for i in range(numberOfVariables):
    for j in range(numberOfVariables):
        covValue = cov(dataDF.iloc[:, i], dataDF.iloc[:, j])
        covMatrix[i][j] = covValue


# Plot the matrix as a heatmap using Seaborn
ax = sn.heatmap(covMatrix, xticklabels=dataDF.columns, yticklabels=dataDF.columns, annot=True)
ax.xaxis.set_ticks_position('top')
plt.show()
