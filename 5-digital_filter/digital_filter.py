"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #5 - Digital Filter
By Jesse Braaksma
22/05/2021
"""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import pi
from cmath import phase


samplingFreq = 600/3

dataFilePath = "5-digital_filter/data.csv"
dataDF = pd.read_csv(dataFilePath, names=['index', 'time', 'signal'], header=0)
signal = dataDF['signal'].tolist()



def DFT(samples):
    ''' Take the Discrete Fourier Transform of a signal, where the signal is a list of values, return as complex narray'''

    numSamples = len(samples)
    frequencyResponse = np.array([]) # Numpy array to hold complex numbers

    # For each frequency (0 to numSamples - 1)
    for k in range(numSamples): # We don't have to use -1 since range does not include the final number of numSamples

        sumRe = 0 # Sum of the real part
        sumIm = 0 # Sum of the imaginary part

        # Sum all samples
        for n in range(numSamples):
            u = -2 * pi * k * n / numSamples
            yRe = samples[n] * np.cos(u) # Real part of frequency response the sample
            yIm = samples[n] * np.sin(u) # Imaginary part of frequency response the sample

            sumRe += yRe
            sumIm += yIm

        z = complex(sumRe, sumIm)
        frequencyResponse = np.append(frequencyResponse, z)

    return frequencyResponse


def calcComplexNumMagnitude(z):
    ''' Return the magnitude of a complex number. '''
    magnitude = np.sqrt(np.square(z.real) + np.square(z.imag))
    return magnitude


dft = DFT(signal)

freqAxis= samplingFreq * (np.linspace(-0.5, 0.5, len(signal)))

dftMag = abs(dft) # Taking the absolute value of a complex number return's it's magitude
dftShift = np.fft.fftshift(dftMag)
dtfPhase = [phase(z) for z in dft]

# Plot the results
fig, axs = plt.subplots(2, 2)
axs[0,0].plot(signal)
axs[0,1].plot(freqAxis, dftShift)
axs[1,0].plot(freqAxis, dtfPhase)
plt.show()