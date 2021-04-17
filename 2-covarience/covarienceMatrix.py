"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #2 - Covarience matrix
By Jesse Braaksma
09/03/2011
"""

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt



dataFilePath = "2-covarience/data.csv"

dataDF = pd.read_csv(dataFilePath, names=['x', 'y', 'z'], header=1)

# Let Pandas do all the work...
corrMatrix = dataDF.corr()

# Plot the matrix as a heatmap using Seaborn
sn.heatmap(corrMatrix, annot=True)
plt.show()