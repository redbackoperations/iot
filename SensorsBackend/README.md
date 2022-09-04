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
npx ts-node ./src/services/sensor-data-processors/speedAndCadence.ts

or

npm run speed-and-cadence-data-processor
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

1. Set your own Basic Auth Creds in `.env` file.

2. Start the local dev server:

```
npm run dev
```

3. Make API calls to read speed and cadence data with Basic Auth credentials. Sample requests are shown below:

```
GET /api/sensors/speed?before=2023-01-01T12:41:22.500Z&after=2022-01-01T12:41:22.500Z&bikeNumber=00001

Response:
{
    "speed": {
        "metadata": {
            "bikeNumber": "00001"
        },
        "_id": "630b72bd70b426c9c0beac2a",
        "reportedAt": "2022-08-28T13:50:53.831Z",
        "value": 12,
        "__v": 0
    }
}

GET /api/sensors/cadence?before=2023-01-01T12:41:22.500Z&after=2022-01-01T12:41:22.500Z&bikeNumber=00002

Response:
{
    "cadence": {
        "metadata": {
            "bikeNumber": "00002"
        },
        "_id": "6313648c0a693e160b9352fb",
        "reportedAt": "2022-09-03T14:28:28.029Z",
        "value": 34444,
        "__v": 0
    }
}


GET /api/sensors/speeds?before=2023-01-01T12:41:22.500Z&after=2022-01-01T12:41:22.500Z&limit=2&bikeNumber=00002

Response:
{
    "speeds": [
        {
            "metadata": {
                "bikeNumber": "00002"
            },
            "_id": "6313626b808c027fc2e7920c",
            "reportedAt": "2022-09-03T14:19:23.527Z",
            "value": 34444,
            "__v": 0
        },
        {
            "metadata": {
                "bikeNumber": "00002"
            },
            "_id": "63134b72cd372c259ec92e84",
            "reportedAt": "2022-09-03T12:41:22.540Z",
            "value": 34444,
            "__v": 0
        }
    ]
}

GET /api/sensors/cadences?before=2023-01-01T12:41:22.500Z&limit=2&bikeNumber=00001

Response:
{
    "cadences": [
        {
            "metadata": {
                "bikeNumber": "00001"
            },
            "_id": "6313654f0a693e160b9352fd",
            "reportedAt": "2022-09-03T14:31:43.529Z",
            "value": 34444,
            "__v": 0
        }
    ]
}

```
