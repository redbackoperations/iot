import * as mqtt from 'mqtt'
import * as dotenv from 'dotenv'
import { IClientOptions } from 'mqtt'

dotenv.config()

const options: IClientOptions = {
  host: process.env.MQTT_HOST,
  port: Number(process.env.MQTT_PORT),
  protocol: process.env.MQTT_PROTOCOL as IClientOptions['protocol'],
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD,
}

// initialize the MQTT client
const mqttClient = mqtt.connect(options)

export default mqttClient
