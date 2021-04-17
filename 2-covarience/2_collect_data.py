import serial, csv

serialPort = 'COM4'

serialConnection = serial.Serial(serialPort, 115200, timeout=.1)

i = 0

with open('2_data.csv', 'w', newline='') as dataFile:
    writer = csv.writer(dataFile)

    while i < 1000:
        while serialConnection.in_waiting > 0:

            readData = serialConnection.readline()[:-2].decode()
            splitData = readData.split(';')

            accX = float(splitData[0])
            accY = float(splitData[1])
            accZ = float(splitData[2])

            print(accX, accY, accZ, i)
            writer.writerow([accX, accY, accZ])

            i = i + 1
