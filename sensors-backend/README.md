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

3. Assign correct MQTT and MongoDB credentials and MQTT topics for reporting devices/sensors data in the `.env` file.

4. Run the device data processor in CLI to initiate the service. For instance, run the following to start up the "device data processor":

```
npx ts-node ./src/services/sensor-data-processors/MQTTFeed.ts

or

npm run device-data-processor
```

5. Manually publish a sensor data MQTT message (with `application/json` content type) via the corresponding MQTT reporting topic you've assigned before. For instance, publish a JSON message via `bike/000001/speed` topic:

```
{
    "bikeId": "631d96630adc9e17cadd73ba",
    "deviceId": "631d96630adc9e17cadd73bb",
    "deviceName": "wahoo cadence sensor #1",
    "unitName": "RPM",
    "value": 36.8,
    "reportedAt": "2022-08-11T01:22:06.471Z",
    "metadata": {
        "firmwareVersion": "1.0.1",
        "staging": true
    }
}
```

Will let `MQTTFeed.ts` processor save a new device data entry with `speed` deviceType in MongoDB as follows:

```
{
  bikeId: new ObjectId("631d96630adc9e17cadd73ba"),
  deviceId: new ObjectId("631d96630adc9e17cadd73bb"),
  deviceName: 'wahoo cadence sensor #1',
  unitName: 'RPM',
  value: 36.8,
  metadata: { firmwareVersion: '1.0.1', staging: true },
  reportedAt: 2022-08-11T01:22:06.471Z,
  _id: new ObjectId("631d9ad7683183250d4b0131"),
  deviceType: 'speed',
  bikeName: '00001',
  createdAt: 2022-09-11T08:22:47.377Z,
  updatedAt: 2022-09-11T08:22:47.377Z,
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

GET /api/device-data?before=2023-01-01T12:41:22.500Z&after=2022-01-01T12:41:22.500Z&bikeName=00001&deviceType=speed

Response:

```
{
    "deviceData": {
        "_id": "631d9cb804ff8d79793f6f83",
        "bikeId": "631d96630adc9e17cadd73ba",
        "deviceId": "631d96630adc9e17cadd73bb",
        "deviceName": "wahoo cadence sensor #1",
        "unitName": "RPM",
        "value": 100.4,
        "metadata": {
            "firmwareVersion": "1.0.1",
            "staging": true
        },
        "reportedAt": "2022-11-12T01:22:06.471Z",
        "deviceType": "speed",
        "bikeName": "00001",
        "createdAt": "2022-09-11T08:30:48.356Z",
        "updatedAt": "2022-09-11T08:30:48.356Z",
        "__v": 0
    }
}
```

GET /api/device-data/many?before=2023-01-01T12:41:22.500Z&after=2022-01-01T12:41:22.500Z&bikeName=00001&deviceType=speed&limit=2

Response:

```
{
    "deviceDatas": [
        {
            "_id": "631d9cb804ff8d79793f6f83",
            "bikeId": "631d96630adc9e17cadd73ba",
            "deviceId": "631d96630adc9e17cadd73bb",
            "deviceName": "wahoo cadence sensor #1",
            "unitName": "RPM",
            "value": 100.4,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "staging": true
            },
            "reportedAt": "2022-11-12T01:22:06.471Z",
            "deviceType": "speed",
            "bikeName": "00001",
            "createdAt": "2022-09-11T08:30:48.356Z",
            "updatedAt": "2022-09-11T08:30:48.356Z",
            "__v": 0
        },
        {
            "_id": "631d9c9c04ff8d79793f6f7d",
            "bikeId": "631d96630adc9e17cadd73ba",
            "deviceId": "631d96630adc9e17cadd73bb",
            "deviceName": "wahoo cadence sensor #1",
            "unitName": "RPM",
            "value": 40,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "staging": true
            },
            "reportedAt": "2022-11-11T01:22:06.471Z",
            "deviceType": "speed",
            "bikeName": "00001",
            "createdAt": "2022-09-11T08:30:20.981Z",
            "updatedAt": "2022-09-11T08:30:20.981Z",
            "__v": 0
        }
    ]
}
```

## How to Seed Data

- To seed bikes data, run the following:

```
npm run seed-bikes-data
```

- To seed devices data, run the following:

```
npm run seed-devices-data
```
