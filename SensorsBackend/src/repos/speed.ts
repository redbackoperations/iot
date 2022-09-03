import { speedModel, ISpeed } from '../models/speed'
import { GET_DATA_MAX_LIMIT } from '../lib/constants'

interface SpeedFilter {
  metadata: { bikeNumber: string }
  reportedAt?: { $lte?: Date; $gte?: Date }
}

/**
 * Get one speed record
 */
const getOne = async ({
  bikeNumber,
  after,
  before,
}: {
  bikeNumber: string
  before?: Date
  after?: Date
}): Promise<ISpeed | null> => {
  // TODO: Add validation rules here

  let filter: SpeedFilter = { metadata: { bikeNumber } }
  // return only the record after a specific time if the 'after' or 'before' param is given
  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

  // find the latest one record for a specific bike
  const speed = await speedModel.findOne(filter).sort({ reportedAt: -1 }).exec()
  return speed
}

/**
 * Get multiple speed records
 */
const getMany = async ({
  bikeNumber,
  after,
  before,
  limit,
}: {
  bikeNumber: string
  before?: Date
  after?: Date
  limit: number
}): Promise<ISpeed[] | null> => {
  // TODO: Add validation rules and pagination here

  // set the returned data limit
  const dataLimit = limit > GET_DATA_MAX_LIMIT ? GET_DATA_MAX_LIMIT : limit

  // return only the records after a specific time if the 'after' or 'before' param is given
  let filter: SpeedFilter = { metadata: { bikeNumber } }
  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

  // find the latest one record for a specific bike
  const speeds = await speedModel.find(filter).sort({ reportedAt: -1 }).limit(dataLimit).exec()
  return speeds
}

export default {
  getOne,
  getMany,
}
