import { sortBy, groupBy } from 'lodash'
import moment from 'moment'
import DeviceData from '../interfaces/device-data'
import { ChartData } from '../interfaces/data-analytics'

const toThousands = (value: number) => {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const availableChartColors = [
  '#8dd3c7',
  'rgb(255, 128, 66)',
  '#bebada',
  '#fb8072',
  '#80b1d3',
  '#fdb462',
  '#b3de69',
  '#fccde5',
  '#d9d9d9',
  '#bc80bd',
  '#ccebc5',
  'rgb(255, 187, 40)',
  'rgb(0, 196, 159)',
]

const generateChartData = (data: DeviceData[]): ChartData[] =>
  sortBy(data, ['reportedAt']).map((deviceData) => ({
    type: deviceData.deviceType,
    value: deviceData.value,
    unit: deviceData.unitName,
    reportedAt: moment.utc(deviceData.reportedAt).format('DD/MM/YYYY HH:mm:ss.SSS'),
  }))

const tokebabCase = (value: string) =>
  value
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase()

const groupChartData = (data: ChartData[]) => groupBy(data, (d) => d.type)

export { toThousands, availableChartColors, generateChartData, groupChartData, tokebabCase }
