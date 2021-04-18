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

deltaT = 0.01


X = [np.matrix([[1], [0], [0], [0]])]

Q = np.matrix([
        [0.0001 , 0 , 0 , 0],
        [0 , 0.0001 , 0 , 0],
        [0 , 0 , 0.0001 , 0],
        [0 , 0 , 0 , 0.0001]
        ])


P = np.identity(4) # Create a 4x4 idendity matrix


R = np.matrix([
        [10 , 0 , 0 , 0],
        [0 , 10 , 0 , 0],
        [0 , 0 , 10 , 0],
        [0 , 0 , 0 , 10]
        ])

q0 = np.matrix([1,0,0,0])

H = np.identity(4) # Create a 4x4 idendity matrix

Pk = np.zeros((4, 4)) # Inital Estimation error covariance

# The Kalman Filter
for k in range(0, len(dataDF) - 1):

    x = X[k]

    p = dataDF.gyro_roll.at[k]
    q = dataDF.gyro_pitch.at[k]
    r = dataDF.gyro_yaw.at[k]

    accelX = dataDF.accel_x.at[k]
    accelY = dataDF.accel_y.at[k]
    accelZ = dataDF.accel_z.at[k]

    O = np.arcsin(accelX / (9.81))                                                 #calculate pitch
    Pi = np.arcsin(-(accelY) / ((9.81)  * (np.cos(O))))                             #calculate roll
    W = 0


    q1 = (np.cos(Pi/2) * np.cos(O/2) * np.cos(W/2)) + (np.sin(Pi/2) * np.sin(O/2) * np.sin(W/2))  #Calculate the quaturnions
    q2 = (np.sin(Pi/2) * np.cos(O/2) * np.cos(W/2)) - (np.cos(Pi/2) * np.sin(O/2) * np.sin(W/2))
    q3 = (np.cos(Pi/2) * np.sin(O/2) * np.cos(W/2)) + (np.sin(Pi/2) * np.cos(O/2) * np.sin(W/2)) 
    q4 = (np.cos(Pi/2) * np.cos(O/2) * np.sin(W/2)) - (np.sin(Pi/2) * np.sin(O/2) * np.cos(W/2))  

    quat = np.matrix([                                                  #quaturnions into a matrix
        [q1],
        [q2],
        [q3],
        [q4]
        ])

    A = H + (deltaT / 2) * np.matrix([
                            [0, -p, -q, -r],
                            [p,  0,  r, -q],
                            [q, -r,  0,  p],
                            [r,  q, -p,  0]
                            ])

    Xk = A * x

    Pk = (A * P * A.T) + Q # Estimation error covariance 

    K = Pk * H.T * (H * Pk * H.T + R)**-1 # Kalman gain

    xNew = Xk + K * (quat - H * Xk)
    X.append(xNew)


roll_arr = []
pitch_arr = []
yaw_arr = []


for x in X:
        #Get output quaternions from prediction results
        q0 = x.item(0)
        q1 = x.item(1)
        q2 = x.item(2)
        q3 = x.item(3)
        
        #Quaternions to Roll
        roll = np.arctan2((2*(q0*q1+q2*q3)),(1-2*(q1**2+q2**2)))    #calculate the quaturnions to roll
        pitch = np.arcsin(2*(q0*q2-q3*q1))                      #calculate the quaturnions to pitch
        yaw = np.arctan2((2*(q0*q3+q1*q2)),(1-2*(q2**2+q3**2))) #calculate the quaturnions to yaw
        
        roll_arr = np.append(roll_arr, roll)
        pitch_arr = np.append(pitch_arr, pitch)
        yaw_arr = np.append(yaw_arr, yaw)



plt.plot(yaw_arr)
plt.show()
