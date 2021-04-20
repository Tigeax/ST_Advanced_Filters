"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #3 - Kalman Filter
By Jesse Braaksma
18/04/2021
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


dataFilePath = "3-kalman_filter/data.csv"
resultsFilePath = "3-kalman_filter/results.csv"

# Get the simulated data from the csv file as a pandas dataframe
dataDF = pd.read_csv(dataFilePath, names=['gyro_roll', 'gyro_pitch', 'gyro_yaw', 'accel_x', 'accel_y', 'accel_z'], header=1)

T = 0.01
g = 9.81 # Grafity

X = [np.matrix([[1], [0], [0], [0]])] # State estimation of the Kalman filter, as a list of matrixes, with inital values

Q = 0.0001 * np.identity(4) # Create a 4x4 idendity matrix, with 0.0001 as it's values
P = np.identity(4) # Create a 4x4 idendity matrix
H = np.identity(4) # Create a 4x4 idendity matrix
R = 10 * np.identity(4)  # Create a 4x4 idendity matrix, with 10 as it's values

q0 = np.matrix([1,0,0,0])

Pk = np.zeros((4, 4)) # Inital Estimation error covariance, 4x4 matrix of zero's


# Lists to hold the results
roll_arr = []
pitch_arr = []
yaw_arr = []


# The Kalman Filter
for k in range(0, len(dataDF)):

    # Previous calculated output
    Xk = X[k]

    # Measured angular velocities
    p = dataDF.gyro_roll.at[k]
    q = dataDF.gyro_pitch.at[k]
    r = dataDF.gyro_yaw.at[k]

    # Measured accelerations
    accelX = dataDF.accel_x.at[k]
    accelY = dataDF.accel_y.at[k]
    accelZ = dataDF.accel_z.at[k]

    O = np.arcsin(accelX / g)                      # Calculate pitch
    Pi = np.arcsin(-(accelY) / (g  * (np.cos(O)))) # Calculate roll
    W = 0                                               # Yaw is always 0

     # Calculate the quaturnions
    quat = np.matrix([
        [(np.cos(Pi/2) * np.cos(O/2) * np.cos(W/2)) + (np.sin(Pi/2) * np.sin(O/2) * np.sin(W/2))],
        [(np.sin(Pi/2) * np.cos(O/2) * np.cos(W/2)) - (np.cos(Pi/2) * np.sin(O/2) * np.sin(W/2))],
        [(np.cos(Pi/2) * np.sin(O/2) * np.cos(W/2)) + (np.sin(Pi/2) * np.cos(O/2) * np.sin(W/2))],
        [(np.cos(Pi/2) * np.cos(O/2) * np.sin(W/2)) - (np.sin(Pi/2) * np.sin(O/2) * np.cos(W/2))  ]
        ])


    # Calculate matrix A
    A = H + (T / 2) * np.matrix([
                                    [0, -p, -q, -r],
                                    [p,  0,  r, -q],
                                    [q, -r,  0,  p],
                                    [r,  q, -p,  0]
                                ])

    Pk = A * Pk * A.T + Q

    K = Pk * H.T * (H * Pk * H.T + R)**-1 # Kalman gain

    XkPlus1 = A * Xk + K * (quat - H * Xk) # State estimation

    Pkplus1 = Pk - K * H * Pk # Estimation error covariance

    X.append(XkPlus1)
    Pk = Pkplus1


    #Get output quaternions from prediction results
    q0 = XkPlus1.item(0)
    q1 = XkPlus1.item(1)
    q2 = XkPlus1.item(2)
    q3 = XkPlus1.item(3)
    
    #Quaternions to roll/pitch/yaw
    roll = np.arctan2((2*(q0*q1+q2*q3)),(1-2*(q1**2+q2**2)))
    pitch = np.arcsin(2*(q0*q2-q3*q1))
    yaw = np.arctan2((2*(q0*q3+q1*q2)),(1-2*(q2**2+q3**2)))
    
    roll_arr = np.append(roll_arr, roll)
    pitch_arr = np.append(pitch_arr, pitch)
    yaw_arr = np.append(yaw_arr, yaw)


dataDF['roll'] = roll_arr
dataDF['pitch'] = pitch_arr
dataDF['yaw'] = yaw_arr


plt.plot(dataDF['yaw'])
plt.show()
