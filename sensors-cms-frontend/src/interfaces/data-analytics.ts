export interface TotalCount {
  bikes: number
  devices: number
  deviceData: number
}

export interface DeviceDataCount {
  speed: number
  cadence: number
  power: number
  ['heart-rate']: number
  resistance: number
  incline: number
  ['head-wind']: number
  [key: string]: number
}

export interface ChartData {
  type: string
  value: number
  unit: string
  reportedAt: string
}

export default TotalCount
