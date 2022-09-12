import * as dotenv from 'dotenv'
import mongoose from 'mongoose'
import { deviceModel } from '../models/device'

dotenv.config()

const data = [
  {
    bikeId: '631dec9e72861e676a001234',
    name: 'Wahoo Speed Sensor # 1',
    label: 'speed-sensor-1',
    description: "the first bike's speed sensor",
    deviceType: 'speed',
    unitName: 'RPM',
    mqttTopicDeviceName: 'speed',
    bluetoothName: 'Wahoo Speed Sensor 111',
    bluetoothUUIDs: [
      {
        name: 'Cycling Power Serivce',
        uuid: 'a026e0370a7d4ab397faf1500f9feb8b',
        characteristics: [
          { name: 'Cycling Power Control Point', uuid: 'a026e1470a7d4ab397faf1500f9feb8b' },
        ],
      },
    ],
    macAddress: '2b:80:12:45:bf:dd',
    metadata: { firmwareVersion: '1.0.1' },
  },
  {
    bikeId: '632dec9e72861e676a001234',
    name: 'Wahoo Cadence Sensor # 2',
    label: 'cadence-sensor-2',
    description: "the second bike's cadence sensor",
    deviceType: 'cadence',
    unitName: 'RPM',
    mqttTopicDeviceName: 'cadence',
    bluetoothName: 'Wahoo Cadence Sensor 222',
    bluetoothUUIDs: [
      {
        name: 'Cycling Power Serivce',
        uuid: 'a026e0270a7d4ab397faf1500f9feb8b',
        characteristics: [
          { name: 'Cycling Power Control Point', uuid: 'a026e1470a4d4ab397faf1500f9feb8b' },
        ],
      },
    ],
    macAddress: '2b:80:12:35:bf:cc',
    metadata: { firmwareVersion: '1.0.1' },
  },
  {
    bikeId: '631dec9e72861e676a001234',
    name: 'Wahoo Kickr Trainer # 1',
    label: 'kickr-trainer-1',
    description: "the first bike's Kickr trainer",
    deviceType: 'resistance',
    unitName: 'percentage',
    mqttTopicDeviceName: 'resistance',
    bluetoothName: 'Wahoo Kickr Trainer 111',
    bluetoothUUIDs: [
      {
        name: 'FTMS Serivce',
        uuid: 'b126e0270a7d4ab397faf1500f9feb8b',
        characteristics: [{ name: 'FTMS Control Point', uuid: 'b136e0270a7d4ab397faf1500f9feb8b' }],
      },
    ],
    macAddress: '2b:80:13:45:cf:dd',
    metadata: { firmwareVersion: '2.0.1' },
  },
  {
    bikeId: '631dec9e72861e676a001234',
    name: 'Wahoo Kickr Climb # 2',
    label: 'kickr-climb-2',
    description: "the first bike's Kickr climb",
    deviceType: 'incline',
    unitName: 'percentage',
    mqttTopicDeviceName: 'incline',
    bluetoothName: 'Wahoo Kickr Climb 222',
    bluetoothUUIDs: [
      {
        name: 'FTMS Serivce',
        uuid: 'b126e0270a7d4ab397faf1500f9feb8b',
        characteristics: [{ name: 'FTMS Control Point', uuid: 'b136e0270a7d4ab397faf1500f9feb8b' }],
      },
      {
        name: 'Custom Serivce for incline control',
        uuid: 'a136e0270a7d4ab397faf1500f9feb8b',
        characteristics: [
          { name: 'Custom Control Point', uuid: 'a136e1270a7d4ab397faf1500f9feb8b' },
        ],
      },
    ],
    macAddress: '2b:82:13:45:bf:dd',
    metadata: { firmwareVersion: '2.0.1' },
  },
]

// connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URL)
  .then(() => {
    console.log('Connected to MongoDB!')

    deviceModel
      .insertMany(data)
      .then(() => {
        console.log('Data inserted:', data)
      })
      .catch((error) => {
        console.error(`Failed to seed devices data`, error)
      })
  })
  .catch((error) => console.error(error))
