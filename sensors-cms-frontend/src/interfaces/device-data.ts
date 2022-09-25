import { DeviceType } from './device'

interface DeviceData {
  _id: string
  bikeId?: string
  deviceId?: string
  workoutId?: string
  userId?: string
  deviceName?: string
  bikeName?: string
  unitName: string
  value: number
  metadata?: object
  reportedAt: string
  deviceType: DeviceType
  createdAt: string
  updatedAt: string
}

export default DeviceData
