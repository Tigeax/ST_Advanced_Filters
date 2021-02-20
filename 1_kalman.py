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


""" Car simulation parameters """
duration = 10           # How long the simulation should run, in seconds
timestep = 0.01          # Timestep between each cycle in the simulation, in seconds
gpsNoise = 10           # The maximum noise in the gps signal, in meters
acceleration = 2        # The acceleration of the car, in m/s2
accelerationNoise = 0.2 # The maximum noise of hte acceleration of the car, in m/s2


""" Create some more parameters based on the constants """
# The average noise should be 0, so create upper and lower limits
gpsNoiseLower = -(gpsNoise / 2)
gpsNoiseUpper = (gpsNoise / 2)
accelerationNoiseLower = -(accelerationNoise / 2)
accelerationUpper = (accelerationNoise / 2)


"""Create car simluation data"""
distanceTravelled = [0] # An array of the true distance in meters the car has traveleled at each timestep
gpsMeasurements = [0] #An array of the distance in meters the car has travelled at each timestep, as measured by the GPS.

carVelocity = 0 # Var to keep track of the car's velocity

for i in range(int((duration - timestep)/timestep)):

    currentAcceleration = acceleration + uniform(accelerationNoiseLower, accelerationUpper)

    carVelocity = carVelocity + (currentAcceleration * timestep)
    
    newDistance = distanceTravelled[i] + (carVelocity * timestep)

    distanceTravelled.append(newDistance)

    newGPSDistanceMeasurement = newDistance + uniform(gpsNoiseLower, gpsNoiseUpper)

    gpsMeasurements.append(newGPSDistanceMeasurement)


plt.plot(distanceTravelled)
plt.plot(gpsMeasurements)
plt.show()


"""Kalman Filter"""


    



