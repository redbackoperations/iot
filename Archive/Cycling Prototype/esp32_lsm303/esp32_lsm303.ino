/*
ESP32 with LSM303 
*/

#include <Wire.h>
#include <LSM303.h>
#include <WiFi.h>
#include <MQTT.h>
#include <ArduinoJson.h>
#include "time.h"

LSM303 accelerometer;

const char ssid[] = "<Enter SSID here>";
const char pass[] = "<Enter Password here>";

// a string to hold NTP server to request epoch time
const char* ntpServer = "pool.ntp.org";

WiFiClient net;
MQTTClient client;

unsigned long lastMillis = 0;

// Get_Epoch_Time() Function that gets current epoch time
unsigned long Get_Epoch_Time() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

void connect() {
  Serial.print("checking wifi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.print("\nconnecting...");
  while (!client.connect("", "", "")) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("\nconnected!");
}

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  
  accelerometer.init();
  accelerometer.enableDefault();

  WiFi.begin(ssid, pass);

  configTime(0, 0, ntpServer);

  // For testing
  // client.begin("broker.hivemq.com", net);
  // Redback Operations MQTT server
  client.begin("34.129.191.60", net);
  connect();
}

void loop()
{
  accelerometer.read();

  // set up json object
  const int capacity = JSON_OBJECT_SIZE(400);
  StaticJsonDocument<capacity> doc;
    
  // Read data and store it in a json object
  doc["sensorID"] = "A1";
  doc["timeStamp"] = Get_Epoch_Time();
  JsonObject sensorData = doc.createNestedObject("sensorData");
  sensorData["acc_x"] = accelerometer.a.x;
  sensorData["acc_y"] = accelerometer.a.y;
  sensorData["acc_z"] = accelerometer.a.z;

  // serialize the json to the jsonString variable
  String jsonString;
  serializeJson(doc, jsonString);

  Serial.println(jsonString);
  delay(100);

  client.loop();
  delay(10);  // <- fixes some issues with WiFi stability

  if (!client.connected()) {
    connect();
  }

  // publish a message roughly every second.
  if (millis() - lastMillis > 1000) {
    lastMillis = millis();
    client.publish("/redback/smartbike/user/accelerometer", jsonString);
  }
}
