import * as dotenv from 'dotenv'
import mongoose from 'mongoose'
import { speedModel } from '../../models/speed'
import { cadenceModel } from '../../models/cadence'
import mqttClient from '../../lib/mqttClient'
import { SPEED_TOPIC_KEY, CADENCE_TOPIC_KEY } from '../../lib/constants'
import { findBikeNumber } from '../../lib/mqttHelper'

dotenv.config()

// setup the callbacks
mqttClient.on('connect', () => {
  console.log('Connected to the MQTT broker!')
})

mqttClient.on('error', (error) => {
  console.log(error)
})

mqttClient.on('message', (topic, message) => {
  // called each time a message is received
  console.log(`[${topic}] Received message:`, message.toString())

  // save Speed data
  if (topic.includes(`/${SPEED_TOPIC_KEY}`)) {
    const speed = new speedModel()
    speed.value = Number(message)
    speed.metadata.bikeNumber = findBikeNumber(topic)

    speed.save((err, doc) => {
      if (err) return console.error('Failed to save a Speed data', err)
      console.log('Saving a new Speed data successfully:', doc)
    })
  }
  // save Cadence data
  else if (topic.includes(`/${CADENCE_TOPIC_KEY}`)) {
    const cadence = new cadenceModel()
    cadence.value = Number(message)
    cadence.metadata.bikeNumber = findBikeNumber(topic)

    cadence.save((err, doc) => {
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
mongoose
  .connect(process.env.MONGODB_URL)
  .then(() => {
    console.log('Connected to MongoDB!')
  })
  .catch((error) => console.error(error))
