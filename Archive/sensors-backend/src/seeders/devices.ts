import * as dotenv from 'dotenv'
import { faker } from '@faker-js/faker'
import mongoose, { Schema } from 'mongoose'
import { randomDeviceTypeAndUnit, randomElement } from '../lib/utils'
import { deviceModel } from '../models/device'
import { bikeModel, IBike } from '../models/bike'

dotenv.config()

const sampleBluetoothUUIDs = [
  {
    name: 'Cycling Power Serivce',
    uuid: 'a026e0370a7d4ab397faf1500f9feb8b',
    characteristics: [
      { name: 'Cycling Power Control Point', uuid: 'a026e1470a7d4ab397faf1500f9feb8b' },
    ],
  },
  {
    name: 'FTMS Serivce',
    uuid: 'b126e0270a7d4ab397faf1500f9feb8b',
    characteristics: [{ name: 'FTMS Control Point', uuid: 'b136e0270a7d4ab397faf1500f9feb8b' }],
  },
  {
    name: 'Custom Serivce for resistance/incline control',
    uuid: 'a136e0270a7d4ab397faf1500f9feb8b',
    characteristics: [{ name: 'Custom Control Point', uuid: 'a136e1270a7d4ab397faf1500f9feb8b' }],
  },
]

const createOne = (bikeIds: Schema.Types.ObjectId[]) => {
  const bikeId = randomElement(bikeIds) as Schema.Types.ObjectId

  const { deviceType, unitName } = randomDeviceTypeAndUnit()
  const deviceName = `Wahoo ${deviceType} sensor/device ${faker.lorem.words()}`

  return {
    bikeId,
    name: deviceName,
    label: `${deviceType}-sensor-${faker.lorem.word()}`,
    description: faker.lorem.sentence(),
    deviceType,
    unitName,
    mqttTopicDeviceName: deviceType,
    bluetoothName: faker.lorem.sentence(),
    bluetoothUUIDs: [randomElement(sampleBluetoothUUIDs)],
    macAddress: faker.internet.mac(),
    metadata: { firmwareVersion: '1.0.1', test: true },
  }
}

const createData = (bikeIds: Schema.Types.ObjectId[], size: number) =>
  Array.from(Array(size).keys()).map(() => createOne(bikeIds))

// connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URL)
  .then(async () => {
    console.log('Connected to MongoDB!\n')

    const bikes = await bikeModel.find().exec()

    if (!bikes || bikes.length === 0) {
      console.log('Error: You need to seed bikes data before seeding devices data!')
      process.exit(1)
    }

    const bikeIds = bikes.map((bike: IBike) => bike._id)
    const data = createData(bikeIds, 20)
    const devices = await deviceModel.insertMany(data)

    console.log('Data inserted:', devices)
    process.exit()
  })
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })
