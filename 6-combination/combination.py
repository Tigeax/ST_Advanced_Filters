import serial, time
import numpy as np
import matplotlib.pyplot as plt

serialPort = 'COM5'

T = 0.01 # 100Hz
g = 9.81 # Gravity


def collectData(serialConnection):

    readData = serialConnection.readline().decode()[:-2]
    splitData = readData.split(';')
    serialConnection.flush()

    accX = float(splitData[0])
    accY = float(splitData[1])
    accZ = float(splitData[2])
    gyroX = float(splitData[3])
    gyroY = float(splitData[4])
    gyroZ = float(splitData[5])
    
    return accX, accY, accZ, gyroX, gyroY, gyroZ


Q = 0.0001 * np.identity(4) # Create a 4x4 idendity matrix, with 0.0001 as it's values
H = np.identity(4)  # Create a 4x4 idendity matrix
R = 10 * np.identity(4)  # Create a 4x4 idendity matrix, with 10 as it's values


def kalmanFilter(X, P, accelX, accelY, accelZ, gyroX, gyroY, gyroZ):

    p = gyroX
    q = gyroY
    r = gyroZ

    Xk = X
    Pk = P

    # Calculate matrix A, from the angular velocities
    A = H + (T / 2) * np.matrix([
                                    [0, -p, -q, -r],
                                    [p,  0,  r, -q],
                                    [q, -r,  0,  p],
                                    [r,  q, -p,  0]
                                ])

    # Calculate pitch/roll/yaw, from the accelerations
    O = np.arcsin(accelX / g)                      # Calculate pitch
    Pi = np.arcsin(-(accelY) / (g  * (np.cos(O)))) # Calculate roll
    W = 0                                          # Yaw is always 0

    # Calculate the quaturnion, from the pitch/roll/yaw
    quat = np.matrix([
        [(np.cos(Pi/2) * np.cos(O/2) * np.cos(W/2)) + (np.sin(Pi/2) * np.sin(O/2) * np.sin(W/2))],
        [(np.sin(Pi/2) * np.cos(O/2) * np.cos(W/2)) - (np.cos(Pi/2) * np.sin(O/2) * np.sin(W/2))],
        [(np.cos(Pi/2) * np.sin(O/2) * np.cos(W/2)) + (np.sin(Pi/2) * np.cos(O/2) * np.sin(W/2))],
        [(np.cos(Pi/2) * np.cos(O/2) * np.sin(W/2)) - (np.sin(Pi/2) * np.sin(O/2) * np.cos(W/2))]
        ])

    Pk = A * Pk * A.T + Q

    K = Pk * H.T * (H * Pk * H.T + R)**-1 # Kalman gain

    newX = A * Xk + K * (quat - H * Xk) # State estimation

    newP = Pk - K * H * Pk # Estimation error covariance

    return newX, newP


def toEulerAngles(X):

    # Get quaternions
    q0 = X.item(0)
    q1 = X.item(1)
    q2 = X.item(2)
    q3 = X.item(3)

    # Quaternions to roll/pitch/yaw
    roll = np.arctan2((2 * (q0 * q1 + q2 * q3)), (1 - 2 * (q1**2 + q2**2)))
    pitch = np.arcsin(2 * (q0 * q2 - q3 * q1))
    yaw = np.arctan2((2 * (q0 * q3 + q1 * q2)), (1 - 2*(q2**2 + q3**2)))
    
    return roll, pitch, yaw


if __name__ == "__main__":

    serialConnection = serial.Serial(serialPort, 115200, timeout=1.0)

    X = np.matrix([[1], [0], [0], [0]]) # Current state of the Kalman filter
    P = np.zeros((4, 4)) # Inital Estimation error covariance, 4x4 matrix of zero's

    fig, axs = plt.subplots(3)

    axs[0].set_title('Roll')
    axs[1].set_title('Pitch')
    axs[2].set_title('Yaw')

    rollList = []
    pitchList = []
    yawList = []

    i = 0

    while True:
        while serialConnection.in_waiting > 0:

            try:
                accX, accY, accZ, gyroX, gyroY, gyroZ = collectData(serialConnection)
            except Exception as e:
                print(e)
                continue

            X, P = kalmanFilter(X, P, accX, accY, accZ, gyroX, gyroY, gyroZ)

            roll, pitch, yaw = toEulerAngles(X)

            roll, pitch, yaw = (180/np.pi) * roll, (180/np.pi) * pitch, (180/np.pi) * yaw

            rollList.append(roll)
            pitchList.append(pitch)
            yawList.append(yaw)

            i = i + 1


        axs[0].plot(rollList, color='b')
        axs[1].plot(pitchList, color='b')
        axs[2].plot(yawList, color='b')

        axs[0].set_xlim(left=max(0, i-950), right=i+20)
        axs[1].set_xlim(left=max(0, i-950), right=i+20)
        axs[2].set_xlim(left=max(0, i-950), right=i+20)

        fig.canvas.draw()

        plt.pause(0.01)

        