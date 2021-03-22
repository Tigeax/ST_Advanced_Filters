#include <M5StickC.h>

float accX = 0.0F;
float accY = 0.0F;
float accZ = 0.0F;

void setup() {

    Serial.begin(115200);

    M5.begin();
    M5.IMU.Init();
    M5.Lcd.setRotation(3);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setTextSize(1);
    M5.Lcd.setCursor(0, 10);
    M5.Lcd.println("  X       Y       Z");
}

void loop() {
    M5.IMU.getAccelData(&accX, &accY, &accZ);

    M5.Lcd.setCursor(0, 30);
    M5.Lcd.printf(" %5.2f   %5.2f   %5.2f   ", accX, accY, accZ);
    M5.Lcd.setCursor(140, 30);
    M5.Lcd.print("G");

    Serial.printf("%5.2f;%5.2f;%5.2f\r\n", accX, accY, accZ);

    delay(10);
}