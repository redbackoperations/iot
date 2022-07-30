/**
 * Program to read data from serial port and publish it over MQTT
 */

const { SerialPort } = require("serialport");
const { ReadlineParser } = require("@serialport/parser-readline");
const mqtt = require("mqtt");

// Connect to mqtt broker
let test_host = "broker.hivemq.com";
let real_host = "34.129.191.60";
let mqtt_port = 1883;
const MQTT_URL = `mqtt://${real_host}:${mqtt_port}`;
const client = mqtt.connect(MQTT_URL);

client.on("connect", () => {
  console.log("Connected to MQTT broker");
});

client.on("error", (error) => {
  console.log(`MQTT Error: ${error}`);
});

// Connect to serial port to receive temperature data
let myPort = new SerialPort({ path: "COM7", baudRate: 9600 });
// Make a new parser to read ASCII lines and pipe the serial stream to the parser
const parser = myPort.pipe(new ReadlineParser({ delimiter: "\r\n" }));

// When new data is available on serial port, publish it to mqtt topic
parser.on("data", (rawData) => {
  jsonObj = JSON.parse(rawData);

  let jsonMsg = {
    timeStamp: Date.now(),
    sensorData: jsonObj.sensorData,
  };

  let topic = `/redback/smartbike/user/${jsonObj.sensorType}`;
  let message = JSON.stringify(jsonMsg);

  client.publish(topic, message, () => {
    console.log(`\nPublished to ${topic}:`);
    console.log(`${message}`);
  });
});
