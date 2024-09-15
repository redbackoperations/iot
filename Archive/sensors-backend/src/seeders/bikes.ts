import * as dotenv from 'dotenv'
import mongoose from 'mongoose'
import { bikeModel } from '../models/bike'

dotenv.config()

const data = [
  {
    name: '000001',
    label: 'bike-01',
    description: 'the first smart bike for Burwood campus',
    mqttTopicPrefix: 'bike/000001',
    mqttReportTopicSuffix: 'report',
  },
  {
    name: '000002',
    label: 'bike-02',
    description: 'the second smart bike for Geelong campus',
    mqttTopicPrefix: 'bike/000002',
    mqttReportTopicSuffix: 'report',
  },
]

// connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URL)
  .then(() => {
    console.log('Connected to MongoDB!\n')

    bikeModel
      .insertMany(data)
      .then(() => {
        console.log('Data inserted:', data)
        process.exit()
      })
      .catch((error) => {
        console.error(`Failed to seed bikes data`, error)
        process.exit(1)
      })
  })
  .catch((error) => console.error(error))
