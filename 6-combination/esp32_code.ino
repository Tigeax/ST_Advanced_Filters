#include <M5StickC.h>

float accX = 0.0F;
float accY = 0.0F;
float accZ = 0.0F;

float gyroX = 0.0F;
float gyroY = 0.0F;
float gyroZ = 0.0F;

void setup() {

    Serial.begin(115200);

    M5.begin();
    M5.IMU.Init();
}

void loop() {
    M5.IMU.getAccelData(&accX, &accY, &accZ);
    M5.IMU.getGyroData(&gyroX, &gyroY, &gyroZ);

    Serial.printf("%5.3f;%5.3f;%5.3f;%5.3f;%5.3f;%5.3f\n", accX, accY, accZ, gyroX, gyroY, gyroZ);

    delay(10);
}