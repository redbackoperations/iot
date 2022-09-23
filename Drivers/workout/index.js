const mqtt = require('mqtt');
require('dotenv').config();

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
const resistanceTopic = 'bike/' + deviceId + '/resistance/control';
const inclineTopic = 'bike/' + deviceId + '/incline/control';
const levelTopic = 'bike/' + deviceId + '/level';

const workout_types = ['ramped', 'strength', 'endurance', 'threshold'];
const command_types = ['start', 'stop', 'increase', 'decrease'];
const min_duration = -1;
const max_duration = 60;

let currentWorkout = '';
let startTime = 0;
let currentResistance = 0;
let currentIncline = 0;
let currentLevel = 1;
let workoutTimer  = 0;

function increaseLevel() {
    currentResistance += 4;
    if (currentResistance > 100)
        currentResistance = 100;
    else
        client.publish(resistanceTopic, currentResistance.toString());

    currentIncline += 1;
    if (currentIncline > 19)
        currentIncline = 19;
    else
        client.publish(inclineTopic, currentIncline.toString());

    currentLevel += 0.5;
    if (currentLevel > 9)
        currentLevel = 9;
    else if (currentLevel === parseInt(currentLevel))
        client.publish(levelTopic, `{"value": ${currentLevel.toString()}}`);

    console.log(`Increased Level to ${currentLevel} Resistance ${currentResistance} Incline ${currentIncline}`);
}

function decreaseLevel() {
    currentResistance -= 4;
    if (currentResistance < 24)
        currentResistance = 24;
    else
        client.publish(resistanceTopic, currentResistance.toString());

    currentIncline -= 1;
    if (currentIncline < 0)
        currentIncline = 0;
    else
        client.publish(inclineTopic, currentIncline.toString());

    currentLevel -= 0.5;
    if (currentLevel < 1)
        currentLevel = 1;
    else if (currentLevel !== parseInt(currentLevel))
        client.publish(levelTopic, `{"value": ${currentLevel.toString()}}`);

    console.log(`Decreased level to ${currentLevel} Resistance ${currentResistance} Incline ${currentIncline}`);
}

// Called at 30 second intervals in the workout.
// Set the resistance and incline as required
function rampedWorkout() {
    increaseLevel();
}

client.on('message', (topic, message) => {
    console.log(`Received ${message}`);
    let obj = JSON.parse(message);

    try {
        // Validation
        if (topic != workoutTopic)
            throw "Invalid topic";
        if (workout_types.indexOf(obj.type) === -1)
            throw "Invalid workout type" + obj.type;
        if (command_types.indexOf(obj.command) === -1)
            throw "Invalid command";
        if ('duration' in obj && (obj.duration < min_duration || obj.duration > max_duration))
            throw "Invalid duration";

        if (currentWorkout === '' && obj.command !== 'start')
            throw "Invalid state";
        if (workout_types.indexOf(currentWorkout) !== -1 && obj.command === 'start')
            throw "Invalid state";
        if (currentWorkout === 'ramped' && (obj.command === 'increase' || obj.command === 'decrease'))
            throw "Invalid state";
         if (currentWorkout !== '' && obj.type !== currentWorkout)
            throw "Invalid state";

        // Parsing
        switch (obj.command) {
        case 'start':
            currentWorkout = obj.type;
            startTime = new Date().getTime();

            console.log("Started " + currentWorkout + " workout at " + startTime.toString());

            currentIncline = 0;
            currentResistance = 24;
            currentLevel = 1;
            client.publish(resistanceTopic, currentResistance.toString());
            client.publish(inclineTopic, currentIncline.toString());
            client.publish(levelTopic, `{"value": ${currentLevel.toString()}}`);

            workoutTimer = setInterval(rampedWorkout, 30000);
            break;

        case 'stop':
            console.log("Stopped " + currentWorkout + " workout at " + new Date().getTime());
            clearInterval(workoutTimer);
            currentWorkout = '';

            currentIncline = 0;
            currentResistance = 24;
            currentLevel = 1;
            client.publish(resistanceTopic, currentResistance.toString());
            client.publish(inclineTopic, currentIncline.toString());
            client.publish(levelTopic, `{"value": ${currentLevel.toString()}}`);
            break;

        case 'increase':
            increaseLevel();
            break;

        case 'decrease':
            decreaseLevel();
            break;
        }

    } catch (e) {
        console.log("Error: " + e);
    }
});

client.on('connect', () => {
    console.log('Connected to broker');
    console.log(`Subscribing to ${workoutTopic}`);
    client.subscribe(workoutTopic);
});
