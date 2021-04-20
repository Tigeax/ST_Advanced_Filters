"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #1 - Kalman Filter
By Jesse Braaksma
17/04/2021
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# File path to the csv files
dataFilePath = "1-kalman_simple/data.csv"
resultsFilePath = "1-kalman_simple/results.csv"

# Get the simulated data from the csv file as a pandas dataframe, only use the first 400 rows as data after this is incorrect.
dataDF = pd.read_csv(dataFilePath, names=['data', 'given_kf'], header=0, nrows=400)

T = 0.1 # Measurements are at 10Hz, so an interval of 0.1 seconds

uk = 1 # The acceleration


# State and output equations matrixes
A = np.matrix([ [1, T],
                [0, 1]])

B = np.matrix([ [T**2/2], 
                [T]])

C = np.matrix([[1,
                0]])


# Noise covarience matrixes
Sw = np.matrix([[0.000001, 0.00002],
                [0.00002,  0.0004]])

Sz = 100

# Create variables for common calcuations in the equations to avoid unnecessary computation
AT = A.T
CT = C.T


Y = dataDF.data.tolist() # Kalman filter input data, gotten from the data.csv file, as a list of floating points
X = [np.matrix([[0], [0]])] # State estimation of the Kalman filter, as a list of matrixes, with inital position and speed set to 0


Pk = np.matrix([[0, 0],
                [0, 0]]) # Inital Estimation error covariance, used in the forloop to keep track of the previous calculation

positionResultList = [0] # A list to contain the position calculated by the KF Filter


# The Kalman Filter
for k in range(0, len(Y) - 1):
    
    Xk = X[k] # Previsous calcluated output
    Ykplus1 = Y[k + 1] # Input

    K = A * Pk * CT * (C * Pk * CT + Sz)**-1 # Kalman Gain

    Xkplus1 = (A * Xk + B * uk) + K * (Ykplus1 - C * Xk) # State estimation

    Pkplus1 = A * Pk * AT + Sw - A * Pk * CT * Sz**-1 * C * Pk * AT # Estimation error covariance

    X.append(Xkplus1) # Add the newly calculated output to the list
    positionResultList.append(Xkplus1.item(0)) # Add the position results that where interested in to the list

    Pk = Pkplus1 # Set the newly calculated Pk to the Pk variable so we can use it in the next loop cycle


# Add the calculated positions to the dataframe
dataDF['calc_kf'] = positionResultList

# Calculate the absolute difference between given and calculated filter and save to dataframe
dataDF['diff_given_calc'] = abs(dataDF['given_kf'] - dataDF['calc_kf'])

# Save the dataframe to the result CSV file
dataDF.to_csv(resultsFilePath)


# Create the plots
fig, axs = plt.subplots(2, 2)

dataDF['data'].plot(ax=axs[0,0], title="Original data", legend=True)
dataDF['given_kf'].plot(ax=axs[0,1], title="Given Kalman Filter", legend=True)
dataDF['calc_kf'].plot(ax=axs[1,0], title="Calculated Kalman Filter", legend=True)
dataDF['diff_given_calc'].plot(ax=axs[1,1], title="Absolute difference between given and calculated filter", legend=True)

plt.show()




