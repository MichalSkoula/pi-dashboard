#include <Wire.h>
#include <M2M_LM75A.h>
#include <Adafruit_BMP085.h>
#include "DHT.h"
#include <ArduinoJson.h>

M2M_LM75A lm75a;
Adafruit_BMP085 bmp180;
DHT dht11(4, DHT11);

const double AirValue = 630;   //you need to replace this value with Value_1
const double WaterValue = 260;  //you need to replace this value with Value_2

const double DarkValue = 526;   //you need to replace this value with Value_1
const double LightValue = 4;  //you need to replace this value with Value_2

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
    float moisture = analogRead(A0);
    moisture = (1 - ((moisture - WaterValue) / (AirValue - WaterValue))) * 100;
    float light = analogRead(A1);
    Serial.println(analogRead(A1));
    light = (1 - ((light - LightValue) / (DarkValue - LightValue))) * 100;

    // json object
    const int capacity = JSON_OBJECT_SIZE(7);
    StaticJsonDocument<capacity> json;

    json["temp1"] = temp1;
    json["temp2"] = temp2;
    json["temp3"] = temp3;
    json["pressure"] = pressure;
    json["humidity"] = humidity;
    json["moisture"] = moisture;
    json["light"] = light;

    serializeJson(json, Serial);

    Serial.println();

    delay(10 * 1000);
}
