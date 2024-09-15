export enum DeviceType {
  speed = 'speed',
  cadence = 'cadence',
  power = 'power',
  heartRate = 'heart-rate',
  resistance = 'resistance',
  incline = 'incline',
  headWind = 'fan',
}

export interface Characteristic {
  name: string
  uuid: string
}

export interface Service extends Characteristic {
  characteristics: Characteristic[]
}

export interface Device {
  bikeId: string
  name: string
  label: string
  description: string
  deviceType: DeviceType
  unitName: string
  mqttTopicDeviceName: string
  macAddress: string
  bluetoothName: string
  bluetoothUUIDs: Service[]
  metadata: object
  createdAt: Date
  updatedAt: Date
}

export default Device
