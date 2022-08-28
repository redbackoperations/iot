import * as mqtt from 'mqtt'
import * as dotenv from 'dotenv'

dotenv.config()

const options = {
  host: process.env.MQTT_HOST,
  port: process.env.MQTT_PORT,
  protocol: process.env.MQTT_PROTOCOL,
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD,
}

// initialize the MQTT client
const mqttClient = mqtt.connect(options)

export default mqttClient
