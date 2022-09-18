import { DeviceType } from '../models/device'
import { deviceDataModel, IDeviceData } from '../models/device-data'
import { GET_DATA_MAX_LIMIT } from '../lib/constants'

interface DeviceDataFilter {
  deviceType?: DeviceType[] | DeviceType
  bikeName?: string
  reportedAt?: { $lte?: Date; $gte?: Date }
  $or?: object[]
  metadata?: object
  value?: { $lte: number; $gte: number }
  bikeId?: string
  ['metadata.testing']?: boolean
}

/**
 * Get one deviceData record
 */
const getOne = async ({
  deviceType,
  bikeName,
  after,
  before,
}: {
  deviceType?: DeviceType
  bikeName?: string
  before?: Date
  after?: Date
}): Promise<IDeviceData | null> => {
  // TODO: Add validation rules here

  let filter: DeviceDataFilter = {}
  if (deviceType) filter = { ...filter, deviceType }
  if (bikeName) filter = { ...filter, bikeName }

  // return only the record after a specific time if the 'after' or 'before' param is given
  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

  // find the latest one record for a specific bike
  const deviceData = await deviceDataModel.findOne(filter).sort({ reportedAt: -1 }).exec()
  return deviceData
}

/**
 * Get multiple deviceData records
 */
const getMany = async ({
  keyword,
  testing,
  deviceTypes,
  valueRange,
  before,
  after,
  bikeName,
  bikeId,
  limit,
}: {
  keyword?: string
  testing?: boolean
  deviceTypes?: DeviceType[]
  valueRange?: [number, number]
  before?: Date
  after?: Date
  bikeName?: string
  bikeId?: string
  limit: number
}): Promise<IDeviceData[] | null> => {
  // TODO: Add validation rules and pagination here

  // set the returned data limit
  const dataLimit = limit > GET_DATA_MAX_LIMIT ? GET_DATA_MAX_LIMIT : limit

  // return only the records after a specific time if the 'after' or 'before' param is given
  let filter: DeviceDataFilter = {}
  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

  // fuzzy search
  if (keyword) {
    filter = {
      ...filter,
      $or: [
        { deviceName: new RegExp(keyword, 'gi') },
        { bikeName: new RegExp(keyword, 'gi') },
        { unitName: new RegExp(keyword, 'gi') },
      ],
    }
  }

  if (testing) {
    filter = {
      ...filter,
      ['metadata.testing']: testing,
    }
  }

  if (deviceTypes) filter = { ...filter, deviceType: deviceTypes }

  if (valueRange) {
    filter = { ...filter, value: { $gte: valueRange[0], $lte: valueRange[1] } }
  }

  if (bikeName) filter = { ...filter, bikeName }
  if (bikeId) filter = { ...filter, bikeId }

  // find the latest one record for a specific bike
  const deviceData = await deviceDataModel
    .find(filter)
    .sort({ reportedAt: -1 })
    .limit(dataLimit)
    .exec()
  return deviceData
}

export default {
  getOne,
  getMany,
}
