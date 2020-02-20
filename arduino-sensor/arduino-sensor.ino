#include <Wire.h>
#include <M2M_LM75A.h>
#include <Adafruit_BMP085.h>
#include "DHT.h"
#include <ArduinoJson.h>

M2M_LM75A lm75a;
Adafruit_BMP085 bmp180;
DHT dht11(4, DHT11);

void setup() {
    lm75a.begin();
    bmp180.begin();
    dht11.begin();

    while (!Serial); // wait for serial monitor  
    Serial.begin(115200);
}

void loop() {
    // get data
    float temp1 = lm75a.getTemperature();
    float temp2 = bmp180.readTemperature();
    float pressure = (bmp180.readPressure() + 32 * 100);
    float temp3 = dht11.readTemperature();
    float humidity = dht11.readHumidity();

    // json object
    const int capacity = JSON_OBJECT_SIZE(5);
    StaticJsonDocument<capacity> json;

    json["temp1"] = temp1;
    json["temp2"] = temp2;
    json["temp3"] = temp3;
    json["pressure"] = pressure;
    json["humidity"] = humidity;

    serializeJson(json, Serial);

    Serial.println();

    delay(10 * 1000);
}
