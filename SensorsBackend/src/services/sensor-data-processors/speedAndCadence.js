import * as dotenv from 'dotenv'
import mongoose from 'mongoose'
import Speed from '../../db/models/speed.js'
import Cadence from '../../db/models/cadence.js'
import mqttClient from '../../lib/mqttClient.js'
import { SPEED_TOPIC_KEY, CADENCE_TOPIC_KEY } from '../../lib/constants.js'
import { findBikeNumber } from '../../lib/mqttHelper.js'

dotenv.config()

// setup the callbacks
mqttClient.on('connect', function () {
  console.log('Connected to the MQTT broker!')
})

mqttClient.on('error', function (error) {
  console.log(error)
})

mqttClient.on('message', function (topic, message) {
  // called each time a message is received
  console.log(`[${topic}] Received message:`, message.toString())

  // save Speed data
  if (topic.includes(`/${SPEED_TOPIC_KEY}`)) {
    const speed = new Speed()
    speed.value = parseFloat(message)
    speed.metadata.bikeNumber = findBikeNumber(topic)

    speed.save(function (err, doc) {
      if (err) return console.error('Failed to save a Speed data', err)
      console.log('Saving a new Speed data successfully:', doc)
    })
  }
  // save Cadence data
  else if (topic.includes(`/${CADENCE_TOPIC_KEY}`)) {
    const cadence = new Cadence()
    cadence.value = parseFloat(message)
    cadence.metadata.bikeNumber = findBikeNumber(topic)

    cadence.save(function (err, doc) {
      if (err) return console.error('Failed to save a Cadence data', err)
      console.log('Saving a new Cadence data successfully:', doc)
    })
  }
  // report error otherwise
  else {
    console.log('Unidentified topic:', topic)
  }
})

// subscribe to speed and cadence topics
mqttClient.subscribe(process.env.MQTT_SPEED_TOPIC)
mqttClient.subscribe(process.env.MQTT_CADENCE_TOPIC)

// connect to MongoDB
await mongoose.connect(process.env.MONGODB_URL)
