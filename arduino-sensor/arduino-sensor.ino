#include <Wire.h>
#include <LM75A.h> //https://github.com/QuentinCG/Arduino-LM75A-Temperature-Sensor-Library
#include <Adafruit_BMP085.h>
#include "DHT.h"
#include <ArduinoJson.h>

// config --------------------------
// humidity
int humidityPin = 4;
DHT dht11(humidityPin, DHT11);

// rain
const double WetValue = 65;
const double DryValue = 0;
int rainPowerPin = 7;
int rainPin = A0;

// moisture
int moisturePin = A2;
const double AirValue = 630;
const double WaterValue = 260;

// light
int lightPin = A1;
const double DarkValue = 1017;
const double LightValue = 2;

// CO
const float COMaxValue = 500;
const float COMinValue = 163;
float CO_sensor = A3;
float CO_value;

// sensors -------------------------
LM75A lm75a;
Adafruit_BMP085 bmp180;

void setup() {
    bmp180.begin();
    dht11.begin();

    pinMode(rainPowerPin, OUTPUT);

    pinMode(CO_sensor, INPUT);
  
    while (!Serial); // wait for serial monitor  
    Serial.begin(115200);
}

void loop() {
    // get data
    float temp1 = lm75a.getTemperatureInDegrees();
    float temp2 = bmp180.readTemperature();
    float pressure = (bmp180.readPressure() + 32 * 100);
    float temp3 = dht11.readTemperature();
    float humidity = dht11.readHumidity();
    
    float moisture = analogRead(moisturePin);
    moisture = (1 - ((moisture - WaterValue) / (AirValue - WaterValue))) * 100;
    
    float light = analogRead(lightPin);
    light = (1 - ((light - LightValue) / (DarkValue - LightValue))) * 100;

    float gas = analogRead(CO_sensor);
    gas = (1 - ((gas - COMaxValue) / (COMinValue - COMaxValue))) * 100;

    // rain
    digitalWrite(rainPowerPin, HIGH);
    delay(1);
    float rain = analogRead(rainPin);
    rain = (rain / WetValue) * 100;
    digitalWrite(rainPowerPin, LOW);
    
    // json object
    const int capacity = JSON_OBJECT_SIZE(9);
    StaticJsonDocument<capacity> json;

    json["temp1"] = temp1;
    json["temp2"] = temp2;
    json["temp3"] = temp3;
    json["pressure"] = pressure;
    json["humidity"] = humidity;
    json["moisture"] = moisture;
    json["light"] = light;
    json["rain"] = rain;
    json["gas"] = gas;

    serializeJson(json, Serial);

    Serial.println();

    delay(10 * 1000);
}
