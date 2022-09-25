import mqtt from 'precompiled-mqtt'
import { IClientOptions } from 'precompiled-mqtt'

const options: IClientOptions = {
  host: process.env.REACT_APP_MQTT_HOST,
  port: Number(process.env.REACT_APP_MQTT_PORT) || 8884,
  protocol: (process.env.REACT_APP_MQTT_PROTOCOL || 'wss') as IClientOptions['protocol'],
  username: process.env.REACT_APP_MQTT_USERNAME,
  password: process.env.REACT_APP_MQTT_PASSWORD,
  hostname: process.env.REACT_APP_MQTT_HOST,
  path: '/mqtt',
}

// initialize the MQTT client
const mqttClient = () => mqtt.connect(options)

export default mqttClient
