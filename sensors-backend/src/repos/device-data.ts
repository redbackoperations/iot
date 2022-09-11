import { DeviceType } from '../models/device'
import { deviceDataModel, IDeviceData } from '../models/device-data'
import { GET_DATA_MAX_LIMIT } from '../lib/constants'

interface DeviceDataFilter {
  deviceType?: DeviceType
  bikeName?: string
  reportedAt?: { $lte?: Date; $gte?: Date }
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
  deviceType,
  bikeName,
  after,
  before,
  limit,
}: {
  deviceType?: DeviceType
  bikeName?: string
  before?: Date
  after?: Date
  limit: number
}): Promise<IDeviceData[] | null> => {
  // TODO: Add validation rules and pagination here

  // set the returned data limit
  const dataLimit = limit > GET_DATA_MAX_LIMIT ? GET_DATA_MAX_LIMIT : limit

  // return only the records after a specific time if the 'after' or 'before' param is given
  let filter: DeviceDataFilter = {}
  if (deviceType) filter = { ...filter, deviceType }
  if (bikeName) filter = { ...filter, bikeName }

  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

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
