import serial, csv

serialPort = 'COM5'

serialConnection = serial.Serial(serialPort, 115200, timeout=.1)

i = 0

with open('data.csv', 'w', newline='') as dataFile:
    writer = csv.writer(dataFile)

    writer.writerow(['index', 'time', 'accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ'])

    while i < 2000:
        while serialConnection.in_waiting > 0:

            readData = serialConnection.readline().decode()[:-2]
            splitData = readData.split(';')
            serialConnection.flush()

            time = int(splitData[0]) / 1000.0
            accX = float(splitData[1])
            accY = float(splitData[2])
            accZ = float(splitData[3])
            gyroX = float(splitData[4])
            gyroY = float(splitData[5])
            gyroZ = float(splitData[6])

            print(i, time, accX, accY, accZ, gyroX, gyroY, gyroZ)
            writer.writerow([i, time, accX, accY, accZ, gyroX, gyroY, gyroZ])

            i = i + 1
