"""
Hanze University of Applied Sciences
Electrical and Electronic Engineering - Major Sensor Technolgyy
Advanced Filters
Assignment #5 - Digital Filter
By Jesse Braaksma
05/06/2021
"""

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# The maximum frequency that we want to keep in the signal
lowpassFilterFreq = 20
highpassFilterFreq = 2

columnToFilter = 'accZ'

# Read the data from the file
dataFilePath = "6-combination/data.csv"
dataDF = pd.read_csv(dataFilePath, usecols=['index', 'time', columnToFilter], header=0)

# Get the signal as a numpy list
signal = dataDF[columnToFilter].to_numpy()

# Get the number of samples
numSamples = dataDF['index'].max()

# Get the sample time
sampleTime = dataDF['time'].max() - dataDF['time'].min()

# Calculate the sampling frequency
samplingFreq = numSamples/sampleTime
print(f"Num samples: {numSamples}")
print(f"Sample time: {sampleTime}")
print(f"Sampling frequency: {samplingFreq}Hz")


# Get the frequencies to display on the x-axis
freqs = samplingFreq * (np.linspace(-0.5, 0.5, len(signal)))

# Get the DFT
dft = np.fft.fft(signal)

# Shift the DFT
dftShifted = np.fft.fftshift(dft)

# Filter the shifted DFT, by setting all values where the frequency is higher then our lowpass frequency to 0
dftShiftedLowpass = dftShifted.copy()
dftShiftedLowpass[(abs(freqs) > lowpassFilterFreq)] = 0

# Filter the shifted DFT, by setting all values where the frequency is lower then our highpass frequency to 0
dftShiftedHighpass = dftShiftedLowpass.copy()
dftShiftedHighpass[(abs(freqs) < highpassFilterFreq)] = 0

# Inverse shift the shifted DFT
dftFilteredInverse = np.fft.ifftshift(dftShiftedHighpass)

# Get the inverse of the DFT to get our filtered signal
signalFiltered = np.fft.ifft(dftFilteredInverse)

# Get the DFT's magnitude's (abs() on a complex number returns it's magnitude)
dftShiftedMag = abs(dftShifted)
dftShiftedFilteredMag = abs(dftShiftedHighpass)


# Plot the results
fig, axs = plt.subplots(2, 2)
fig.tight_layout()

axs[0,0].set_title('Signal')
axs[0,0].set(xlabel='time (s)')
axs[0,0].plot(dataDF['time'], signal)

axs[0,1].set_title('DFT')
axs[0,1].set(xlabel='Frequency (Hz)', ylabel='Magnitude')
axs[0,1].plot(freqs, dftShiftedMag)

axs[1,0].set_title('Filtered DFT')
axs[1,0].set(xlabel='Frequency (Hz)', ylabel='Magnitude')
axs[1,0].plot(freqs, dftShiftedFilteredMag)

axs[1,1].set_title('Filtered signal')
axs[1,1].set(xlabel='time (s)')
axs[1,1].plot(dataDF['time'], signalFiltered)

plt.show()