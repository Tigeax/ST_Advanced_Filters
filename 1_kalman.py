"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #1 - Kalman Filter
By Jesse Braaksma
20/02/2011
"""

import matplotlib.pyplot as plt
from random import uniform
import numpy as np
import pandas as pd

dataFilePath = "1_kalman_data.csv"
resultsFilePath = "1_kalman_results.csv"

postitionError = 10
postitionErrorLower = -(postitionError / 2)
postitionErrorUpper =  (postitionError / 2)
accelNoise = 0.2
accelNoiseLower = -(accelNoise / 2)
accelNoiseUpper =  (accelNoise / 2)
freq = 10.0
T = 1.0/freq
duration = 30
N = int(duration/T)

A = np.matrix([[1.0, T], [0.0, 1.0]])
AT = A.T
B = np.matrix([[T**2.0/2.0], [T]])
C = np.matrix([[1.0, 0.0]])
CT = C.T

accel = 1.0

Sw = np.matrix([[0.000001, 0.00002], [0.00002, 0.0004]])
Sz = np.matrix([[100.0]])
SzInv = np.linalg.inv(Sz)


def getSimulatedData():

    stateList = [np.matrix([[0], [0]])]
    positionList = [0]
    actualPostList = [0]

    for k in range(N):
        state = stateList[k]

        posNoiseK = uniform(postitionErrorLower, postitionErrorUpper)
        accelNoiseK = uniform(accelNoiseLower, accelNoiseUpper)
        
        nextState = A.dot(state) + B * (accel + accelNoiseK)
        actualPostList.append(nextState.item(0))
        nextPosition = C.dot(nextState).item(0) + posNoiseK

        stateList.append(nextState)
        positionList.append(nextPosition)

        return positionList


def getDataCSV():
    dataDF = pd.read_csv(dataFilePath, usecols=['data', 'precalculated'])
    return dataDF



def KF(positionList):

    P = np.matrix([[0.0, 0.0], [0.0, 0.0]]) #estimation error covariance
    X = np.matrix([[0.0], [0.0]])
    stateEstimateList = [0.0]

    for k in range(len(positionList) - 1):

        K = A.dot(P).dot(CT).dot(np.linalg.inv(C.dot(P).dot(CT) + Sz))

        nextX = (A * X + B * accel) + K.dot(positionList[k + 1] - C * X)

        nextP = A.dot(P).dot(AT) + Sw - A.dot(P).dot(CT).dot(SzInv).dot(C).dot(P).dot(AT)

        X = nextX
        P = nextP

        stateEstimateList.append(X.item(0))

    return stateEstimateList

if __name__ == "__main__":
    dataDF = getDataCSV()
    kfResult = KF(dataDF['data'].tolist())
    dataDF['result'] = kfResult
    dataDF.to_csv(resultsFilePath)