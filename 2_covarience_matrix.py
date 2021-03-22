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

df = pd.read_csv("2_data.csv")

df.columns = ['x','y','z']

corrMatrix = df.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()