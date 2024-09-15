import * as dotenv from 'dotenv'
import mongoose from 'mongoose'
import moment from 'moment'
import { deviceDataModel, IMQTTDeviceData } from '../../models/device-data'
import mqttClient from '../../lib/mqttClient'
import { DEVICE_DATA_TOPICS } from '../../lib/constants'
import { findBikeNumber, deviceNameFromTopic } from '../../lib/mqttHelper'
import { DeviceType } from '../../models/device'

dotenv.config()

// setup the callbacks
mqttClient.on('connect', () => {
  console.log('Connected to the MQTT broker!')
})

mqttClient.on('error', (error) => {
  console.log(error)
})

// the message needs to be a JSON type to be able to retrive device data value, device name, device_type, unit name, user id, bike id workout id, etc in one go
mqttClient.on('message', (topic, message) => {
  // called each time a message is received
  console.log(`[${topic}] Received message:`, message.toString())

  // save device data
  const deviceNamePart = deviceNameFromTopic(topic)
  const deviceType = DEVICE_DATA_TOPICS.find((deviceDataTopic) =>
    deviceDataTopic.match(deviceNamePart)
  )

  if (deviceType) {
    try {
      const payload = JSON.parse(message.toString()) as IMQTTDeviceData

      const deviceData = new deviceDataModel(payload)
      // ensure to convert value from string to float number
      deviceData.value = Number(payload.value)
      // manually assign device type
      deviceData.deviceType = deviceType as DeviceType
      // manually assign bike name if not provided
      if (!payload.bikeName) deviceData.bikeName = findBikeNumber(topic)
      // assign reportedAt if it's passed from the message payload
      if (!payload.timestamp || !payload.reportedAt) {
        deviceData.reportedAt = moment
          .unix((payload.timestamp || payload.reportedAt) as unknown as number)
          .toDate()
      }

      deviceData.save((err, doc) => {
        if (err) return console.error(`[${topic}] Failed to save a device data`, err)
        console.log('Saving a new device data successfully:', doc)
      })
    } catch (err) {
      console.error(`[${topic}] Failed to save a device data`, err)
    }
  }
  // report error otherwise
  else {
    console.log('Unidentified topic:', topic)
  }
})

// subscribe to all topics as per MQTTv2 PowerPoint Presentation
// TODO: get all topics from Bike/Device DB records instead
mqttClient.subscribe(process.env.MQTT_SPEED_TOPIC)
mqttClient.subscribe(process.env.MQTT_CADENCE_TOPIC)
mqttClient.subscribe(process.env.MQTT_POWER_TOPIC)
mqttClient.subscribe(process.env.MQTT_HEART_RATE_TOPIC)
mqttClient.subscribe(process.env.MQTT_RESISTANCE_TOPIC)
mqttClient.subscribe(process.env.MQTT_INCLINE_TOPIC)
mqttClient.subscribe(process.env.MQTT_FAN_TOPIC)

// connect to MongoDB
mongoose
  .connect(process.env.MONGODB_URL)
  .then(() => {
    console.log('Connected to MongoDB!')
  })
  .catch((error) => console.error(error))
