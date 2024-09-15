import * as dotenv from 'dotenv'
import mongoose, { Schema } from 'mongoose'
import { faker } from '@faker-js/faker'
import { bikeModel, IBike } from '../models/bike'
import { deviceModel, IDevice } from '../models/device'
import { deviceDataModel } from '../models/device-data'
import { randomElement } from '../lib/utils'

dotenv.config()

const createOne = (bikeIds: Schema.Types.ObjectId[], devices: IDevice[]) => {
  const bikeId = randomElement(bikeIds) as Schema.Types.ObjectId
  const device = randomElement(devices) as IDevice
  const deviceName = `Wahoo ${device.deviceType} sensor/device ${faker.lorem.words()}`
  const unitName = device.unitName
  const value = faker.datatype.number({ min: 0, max: 200 })

  return {
    bikeId,
    deviceId: device._id,
    deviceName,
    deviceType: device.deviceType,
    unitName,
    value,
    metadata: { firmwareVersion: '1.0.1', testing: true },
    // reportedAt: randomDate(new Date(2022, 9, 1), new Date(2022, 9, 3)),
    reportedAt: faker.date.past(0, '2022-09-15T00:00:00.000Z'),
  }
}

const createData = (bikeIds: Schema.Types.ObjectId[], devices: IDevice[], size: number) =>
  Array.from(Array(size).keys()).map(() => createOne(bikeIds, devices))

// connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URL)
  .then(async () => {
    console.log('Connected to MongoDB!\n')

    const bikes = await bikeModel.find().exec()
    if (!bikes || bikes.length === 0) {
      console.log('Error: You need to seed bikes data before seeding sensors data!')
      process.exit(1)
    }

    const devices = await deviceModel.find().exec()
    if (!devices || devices.length === 0) {
      console.log('Error: You need to seed devices data before seeding sensors data!')
      process.exit(1)
    }

    const bikeIds = bikes.map((bike: IBike) => bike._id)
    const data = createData(bikeIds, devices, 1000)
    const deviceData = await deviceDataModel.insertMany(data)

    console.log('Data inserted:', deviceData)
    process.exit()
  })
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })
