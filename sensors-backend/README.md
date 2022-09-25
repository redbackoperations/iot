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

npm run iot-data-processor
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

GET /api/device-data/many?limit=5&before=2022-09-18T04:48:49.656Z&deviceTypes[]=incline&deviceTypes[]=power&valueRange[]=50&valueRange[]=120&after=2021-01-19T00:48:49.656Z&keyword=Wahoo&bikeId=632585c4ef34d8b46d451edc

Response:

```
{
    "total": 5,
    "deviceData": [
        {
            "_id": "632586e26ee8f0a42b513c1e",
            "bikeId": "632585c4ef34d8b46d451edc",
            "deviceId": "632585cc0e9bb0d67f3ae132",
            "deviceType": "incline",
            "deviceName": "Wahoo incline sensor/device repellendus totam veritatis",
            "unitName": "degree",
            "value": 107,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "test": true
            },
            "reportedAt": "2022-09-14T09:11:06.961Z",
            "__v": 0,
            "createdAt": "2022-09-17T08:35:46.893Z",
            "updatedAt": "2022-09-17T08:35:46.893Z"
        },
        {
            "_id": "63258be3830f74e250707574",
            "bikeId": "632585c4ef34d8b46d451edc",
            "deviceId": "632585cc0e9bb0d67f3ae11d",
            "deviceType": "incline",
            "deviceName": "Wahoo incline sensor/device unde consequatur est",
            "unitName": "degree",
            "value": 117,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "test": true
            },
            "reportedAt": "2022-09-13T23:10:31.892Z",
            "__v": 0,
            "createdAt": "2022-09-17T08:57:07.663Z",
            "updatedAt": "2022-09-17T08:57:07.663Z"
        },
        {
            "_id": "63258be3830f74e25070744f",
            "bikeId": "632585c4ef34d8b46d451edc",
            "deviceId": "632585cc0e9bb0d67f3ae141",
            "deviceType": "incline",
            "deviceName": "Wahoo incline sensor/device quis at facere",
            "unitName": "degree",
            "value": 81,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "test": true
            },
            "reportedAt": "2022-09-13T21:17:39.604Z",
            "__v": 0,
            "createdAt": "2022-09-17T08:57:07.653Z",
            "updatedAt": "2022-09-17T08:57:07.653Z"
        },
        {
            "_id": "6325d6da5aaf35bc80a9b135",
            "bikeId": "632585c4ef34d8b46d451edc",
            "deviceId": "63258edb04250d78a8ad1684",
            "deviceType": "power",
            "deviceName": "Wahoo power sensor/device modi in reiciendis",
            "unitName": "W",
            "value": 68,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "test": true
            },
            "reportedAt": "2022-09-13T20:22:41.942Z",
            "__v": 0,
            "createdAt": "2022-09-17T14:16:58.714Z",
            "updatedAt": "2022-09-17T14:16:58.714Z"
        },
        {
            "_id": "63258ee3b0bc8ff18fd0e86f",
            "bikeId": "632585c4ef34d8b46d451edc",
            "deviceId": "632585cc0e9bb0d67f3ae117",
            "deviceType": "incline",
            "deviceName": "Wahoo incline sensor/device qui odit possimus",
            "unitName": "degree",
            "value": 79,
            "metadata": {
                "firmwareVersion": "1.0.1",
                "test": true
            },
            "reportedAt": "2022-09-13T08:13:33.388Z",
            "__v": 0,
            "createdAt": "2022-09-17T09:09:55.619Z",
            "updatedAt": "2022-09-17T09:09:55.619Z"
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

- To seed sensors data, run the following:

```
npm run seed-sensors-data
```
