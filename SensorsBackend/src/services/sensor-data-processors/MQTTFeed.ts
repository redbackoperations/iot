import * as dotenv from 'dotenv'
import mongoose from 'mongoose'
import { speedModel } from '../../models/speed'
import { cadenceModel } from '../../models/cadence'
import { powerModel } from '../../models/power'
import { heartrateModel } from '../../models/heartrate'
import { resistanceModel } from '../../models/resistance'
import { inclineModel } from '../../models/incline'
import { inclineModel } from '../../models/fan'
import mqttClient from '../../lib/mqttClient'
import { SPEED_TOPIC_KEY, CADENCE_TOPIC_KEY, POWER_TOPIC_KEY, HEARTRATE_TOPIC_KEY, RESISTANCE_TOPIC_KEY, INCLINE_TOPIC_KEY, FAN_TOPIC_KEY } from '../../lib/constants'
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
    // save Power data
    else if (topic.includes(`/${POWER_TOPIC_KEY}`)) {
        const power = new powerModel()
        power.value = Number(message)
        power.metadata.bikeNumber = findBikeNumber(topic)
    
        power.save((err, doc) => {
          if (err) return console.error('Failed to save a Power data', err)
          console.log('Saving a new Power data successfully:', doc)
        })
    }
    // save Heartrate data
    else if (topic.includes(`/${HEARTRATE_TOPIC_KEY}`)) {
        const heartrate = new heartrateModel()
        heartrate.value = Number(message)
        heartrate.metadata.bikeNumber = findBikeNumber(topic)
    
        heartrate.save((err, doc) => {
          if (err) return console.error('Failed to save a Heartrate data', err)
          console.log('Saving a new Heartrate data successfully:', doc)
        })
    }
    // save Resistance data
    else if (topic.includes(`/${RESISTANCE_TOPIC_KEY}`)) {
        const resistance = new resistanceModel()
        resistance.value = Number(message)
        resistance.metadata.bikeNumber = findBikeNumber(topic)
    
        resistance.save((err, doc) => {
          if (err) return console.error('Failed to save a Resistance data', err)
          console.log('Saving a new Resistance data successfully:', doc)
        })
    }
    // save Incline data
    else if (topic.includes(`/${INCLINE_TOPIC_KEY}`)) {
        const incline = new inclineModel()
        incline.value = Number(message)
        incline.metadata.bikeNumber = findBikeNumber(topic)
    
        incline.save((err, doc) => {
          if (err) return console.error('Failed to save a Incline data', err)
          console.log('Saving a new Incline data successfully:', doc)
        })
    }
    // save Fan data
    else if (topic.includes(`/${FAN_TOPIC_KEY}`)) {
      const fan = new fanModel()
      fan.value = Number(message)
      fan.metadata.bikeNumber = findBikeNumber(topic)
  
      fan.save((err, doc) => {
        if (err) return console.error('Failed to save a Fan data', err)
        console.log('Saving a new Fan data successfully:', doc)
      })
    }
    // report error otherwise
    else {
      console.log('Unidentified topic:', topic)
    }
  })

// subscribe to all topics as per MQTTv2 PowerPoint Presentation
mqttClient.subscribe(process.env.MQTT_SPEED_TOPIC)
mqttClient.subscribe(process.env.MQTT_CADENCE_TOPIC)
mqttClient.subscribe(process.env.MQTT_POWER_TOPIC)
mqttClient.subscribe(process.env.MQTT_HEARTRATE_TOPIC)
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