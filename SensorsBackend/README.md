# Sensors Backend

#### The backend service for storing sensors data and providing APIs to expose those data

---

## Prerequisite

1. Please ensure `Nodejs`(>= v16.0.0) and `npm`(>=7.0.0) have been installed.

2. Please make sure you have MQTT broker details ready.

3. Please make sure you have a MongoDB server ready for use.

## How to Run and Manually Test A Sensor Data Processor Locally

1. Run `npm install` to install all needed packages.

2. Create a new `.env` file in the root path, and copy `.env.example` keys to the file.

3. Assign correct MQTT and MongoDB credentials and MQTT topics for reporting sensors data in the `.env` file.

4. Run a sensor data processor in CLI to initiate the service. For instance, run the following to start up the "speed and cadence data processor":

```
 node ./src/services/sensor-data-processors/speedAndCadence.js
```

5. Manually publish a sensor data MQTT message via the corresponding MQTT reporting topic you've assigned before. For instance, publish a `20.0` message via `bike/000001/speed` topic will let `speedAndCadence.js` processor save a new Speed data entry in MongoDB as follows:

```
 {
  metadata: { bikeNumber: '000001' },
  _id: new ObjectId("630b72fdc87d35ffa6ab3e1a"),
  reportedAt: 2022-08-28T13:51:57.093Z,
  value: 20.0,
  __v: 0
}
```

## How to Test A Sensor Data API

TBC...
