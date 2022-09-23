const mqtt = require('mqtt');
require('dotenv').config()

const mqtt_credentials = {
    host: process.env.MQTT_HOSTNAME || "localhost",
    port: 8883,
    protocol: "mqtts",
    username: process.env.MQTT_USERNAME || "",
    password: process.env.MQTT_PASSWORD || ""
};

const client = mqtt.connect(mqtt_credentials);

const deviceId = process.env.DEVICE_ID || "invalid";
const workoutTopic = 'bike/' + deviceId + '/workout';

const payloadStart = '{"type": "ramped", "command": "start", "duration": -1}';
const payloadStop = '{"type": "ramped", "command": "stop"}';

function stopWorkout() {
    console.log(`Publishing ${workoutTopic} ${payloadStop}`);
    client.publish(workoutTopic, payloadStop);
}

client.on('connect', () => {
    console.log('Connected to broker');
    console.log(`Publishing ${workoutTopic} ${payloadStart}`);
    client.publish(workoutTopic, payloadStart);
    // Stop the timeout after 11 minutes
    setTimeout(stopWorkout, 660000);
});
