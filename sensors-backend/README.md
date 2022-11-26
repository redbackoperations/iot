# IoT Sensors Data Backend

This is a composite set of backend services from IoT team for storing sensors data into DB and providing essential REST APIs to expose/manage those data for **IoT CMS Frontend** application or other teams to use.

## Key Features

1. The core IoT sensor data DB schemas are clearly defined in `/src/models/` folder, including `Bike`, `Device` and `DeviceData` schemas.
2. A "sensors data processor" (`src/services/sensor-data-processors/MQTTFeed.ts`) to actively store sensors data into **MongoDB** as "time series" collection data with correct `deviceType`, `unitName`, `value` and `reportedAt` attributes payload whenever it receiving a MQTT sensor data report message from a MQTT topic like `bike/000001/speed` or `bike/000002/resistance`.
3. Multiple REST APIs, provisioned by **ExpressJS**, to be able to read/create/update `Bike`, `Device` and `DeviceData`, such as:
   - `GET /api/data-analytics/total-count`
   - `GET /api/data-analytics/device-data/total-count`
   - `GET /api/bikes`
   - `GET /api/bike?id={bike_id}`
   - `POST /api/bikes`
   - `PUT /api/bikes/{bike_id}`
   - `GET /api/devices`
   - `GET /api/device?id={device_id}`
   - `POST /api/devices`
   - `PUT /api/devices/{device_id}`
   - `GET /api/device-data?before=2023-01-01T12:41:22.500Z&bikeName=000001&deviceType=speed`
   - `GET /api/device-data/many?keyword=wahoo&testing=true&deviceTypes[]=cadence&deviceTypes[]=resistance&before=2022-09-25T06:22:28.404Z&limit=50`
4. Both the "sensors data processor" and the API server can be run as separate `Nodejs` processes using this exact same monolith repo.
5. "IoT data seeders" to feed some fake `Bike`, `Device` and `DeviceData` data into MongoDB (`src/seeders/`).

## Prerequisite

1. Please ensure `Nodejs`(>= v16.0.0) and `npm`(>=7.0.0) have been installed.

2. Please make sure you have MQTT broker details ready.

3. Please make sure you have a MongoDB server with credentials ready for use.

4. To build a new version of docker image, you will also need to install `Docker` locally.

## How to Install

1. Run `npm install` to install all needed packages.

2. Create a new `.env` file in the root path, and copy `.env.example` values to the file.

3. Assign correct MQTT and MongoDB credentials and MQTT topics for reporting devices/sensors data in the `.env` file.

## How to Run the Sensor Data Processor

1. Run the "sensors data processor" in CLI to initiate the service:

```
npx ts-node ./src/services/sensor-data-processors/MQTTFeed.ts

or

npm run iot-data-processor
```

2. Manually publish a sensor data MQTT message (with `application/json` content type) via the corresponding MQTT reporting topic you've assigned before. For instance, publish a JSON message via `bike/000001/speed` topic like

```
{
    "bikeId": "631d96630adc9e17cadd73ba",
    "deviceId": "631d96630adc9e17cadd73bb",
    "deviceName": "wahoo cadence sensor #1",
    "unitName": "m/s",
    "value": 36.8,
    "reportedAt": "2022-08-11T01:22:06.471Z",
    "metadata": {
        "firmwareVersion": "1.0.1",
        "staging": true
    }
}
```

Will let the "sensors data processor" save a new device data entry with `speed` deviceType in MongoDB as follows:

```
{
  bikeId: new ObjectId("631d96630adc9e17cadd73ba"),
  deviceId: new ObjectId("631d96630adc9e17cadd73bb"),
  deviceName: 'wahoo cadence sensor #1',
  unitName: 'm/s',
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

## How to Run the Sensor Data APIs Server

1. Set your own Basic Auth Creds in `.env` file.

2. Start the local dev server:

```
npm run dev
```

3. Make API calls to read **single/multiple** sensors/devices' data with Basic Auth credentials. Sample requests are shown below:

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

## How to Feed Data Using "IoT data seeders"

- To feed `bikes` data, run the following:

```
npm run seed-bikes-data
```

- To feed devices data, run the following:

```
npm run seed-devices-data
```

- To feed sensors data, run the following:

```
npm run seed-sensors-data
```

## How to Create a New Docker Image and Push to GCP Container Registry

### For the API server:

1. You need to refer to the official GCP docker docs to authenticate your GCP account locally with Docker first.

2. Under the root folder directory, run `docker build -t cms-be .` to create a new docker image build.

3. Assign the new build with a new docker tag version like: `docker tag cms-be {YOUR_GCP_REGION_URL_HERE}/{YOUR_GCP_PROJECT_ID_HERE}/cms-be:v0.1`.

4. Push the docker image to GCP with `{YOUR_GCP_REGION_URL_HERE}/{YOUR_GCP_PROJECT_ID_HERE}/cms-be:v0.1`.

5. Now you can pull the newly pushed docker image on the GCP VM instance, stop the old docker container, and start a new container with this new image build. The production IoT FE app is running the latest version build now.

### For the Sensors Data Processor:

1. You can follow the same steps as above with just some slight changes in the docker commands:

   - The docker build command needs to be updated to: `docker build -f ./Dockerfile.iot-data-processor -t iot-data-processor .`
   - Change the docker image name from `cms-be` to `iot-data-processor`.

## Extra Notes

- Both the API server and "sensors data processor" are now hosted on a GCP Compute Engine VM instance.
- The APIs can now be visited at `http://34.129.10.237:3000` with proper Basic Auth creds.
