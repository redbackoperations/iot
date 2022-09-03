import { cadenceModel, ICadence } from '../models/cadence'
import { GET_DATA_MAX_LIMIT } from '../lib/constants'

interface CadenceFilter {
  metadata: { bikeNumber: string }
  reportedAt?: { $lte?: Date; $gte?: Date }
}

/**
 * Get one cadence record
 */
const getOne = async ({
  bikeNumber,
  after,
  before,
}: {
  bikeNumber: string
  before?: Date
  after?: Date
}): Promise<ICadence | null> => {
  // TODO: Add validation rules here

  let filter: CadenceFilter = { metadata: { bikeNumber } }
  // return only the record after a specific time if the 'after' or 'before' param is given
  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

  console.log(filter)

  // find the latest one record for a specific bike
  const cadence = await cadenceModel.findOne(filter).sort({ reportedAt: -1 }).exec()
  return cadence
}

/**
 * Get multiple cadence records
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
}): Promise<ICadence[] | null> => {
  // TODO: Add validation rules and pagination here

  // set the returned data limit
  const dataLimit = limit > GET_DATA_MAX_LIMIT ? GET_DATA_MAX_LIMIT : limit

  // return only the records after a specific time if the 'after' or 'before' param is given
  let filter: CadenceFilter = { metadata: { bikeNumber } }
  if (before) filter = { ...filter, reportedAt: { $lte: before } }
  if (after) filter = { ...filter, reportedAt: { ...filter.reportedAt, $gte: after } }

  // find the latest one record for a specific bike
  const cadences = await cadenceModel.find(filter).sort({ reportedAt: -1 }).limit(dataLimit).exec()
  return cadences
}

export default {
  getOne,
  getMany,
}
