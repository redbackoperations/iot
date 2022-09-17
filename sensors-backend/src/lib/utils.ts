import { DeviceType, DeviceTypeUnitNames } from '../models/device'

const randomElement = (array: any[]): any => array[Math.floor(Math.random() * array.length)]

const randomDeviceTypeAndUnit = () => {
  const deviceType = randomElement(Object.values(DeviceType)) as string
  const indexOfDeviceType = Object.values(DeviceType).indexOf(deviceType as DeviceType)
  const unitName = Object.values(DeviceTypeUnitNames)[indexOfDeviceType]

  return { deviceType, unitName }
}

const randomDate = (start: Date, end: Date): Date => {
  return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()))
}

export { randomElement, randomDeviceTypeAndUnit, randomDate }
