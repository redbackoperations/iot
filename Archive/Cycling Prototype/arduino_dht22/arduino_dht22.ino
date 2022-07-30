#include <DHT.h>
#include <DHT_U.h>
#include <ArduinoJson.h>

//Constants
#define DHTPIN 2     // Digital pin 2
#define DHTTYPE DHT22 

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  dht.begin();
  Serial.begin(9600);
}

void loop() {
  // get the temperature every 5 seconds
  delay(5000);

  // set up json object
  const int capacity = JSON_OBJECT_SIZE(16);
  StaticJsonDocument<capacity> doc;
  doc["sensorType"] = "temperature_humidity";

  // Read data and store it in a json object
  JsonObject sensorData = doc.createNestedObject("sensorData");
  sensorData["temperature"] = dht.readTemperature();
  sensorData["humidity"] = dht.readHumidity();

  // serialize the json to the jsonString variable
  String jsonString;
  serializeJson(doc, jsonString);

  // print the value to the console
  Serial.println(jsonString);
}
