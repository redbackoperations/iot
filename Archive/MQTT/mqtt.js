const mqtt = require("mqtt");
require('dotenv').config()

// MQTT Credentials
var mqtt_credentials = {
  host: process.env.MQTT_HOST || "localhost",
  port: 8883,
  protocol: "mqtts",
  username: process.env.MQTT_USERNAME || "",
  password: process.env.MQTT_PASSWORD || "",
};

const client = mqtt.connect(mqtt_credentials);

let test_topic = 'smartbike/test'
let test_message = 'This is a test message.'

client.on("connect", () => {
  console.log("Connected to MQTT broker")
  /**
   * General Topic Structure:
   * smartbike/{deviceType}/{deviceID}
   * 
   * Message - JSON strings:
   * {
   *   username: {userName},
   *   data: { }
   * }
   */
  client.subscribe(`smartbike/+/+`);

  client.publish(test_topic, test_message, () => {
    console.log(`\nPublished to ${test_topic}:`);
    console.log(`${test_message}`);
  });
});

client.on("error", (error) => {
  console.log(`MQTT Error: ${error}`);
});

client.on("message", (topic, message, packet) => {
    
});