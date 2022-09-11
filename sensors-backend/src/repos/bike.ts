import { bikeModel, IBike } from '../models/bike'

interface BikeFilter {
  name?: string
  _id?: string
}

/**
 * Get one bike record
 */
const getOne = async ({ name, _id }: BikeFilter): Promise<IBike | null> => {
  let filter: BikeFilter = {}
  if (name) filter = { ...filter, name }
  if (_id) filter = { ...filter, _id }

  // find the latest one record for a specific bike
  const bike = await bikeModel.findOne(filter).sort({ createdAt: -1 }).exec()
  return bike
}

/**
 * Get multiple bike records
 */
const getMany = async ({ name, _id }: BikeFilter): Promise<IBike[] | null> => {
  let filter: BikeFilter = {}
  if (name) filter = { ...filter, name }
  if (_id) filter = { ...filter, _id }

  const bikes = await bikeModel.find(filter).sort({ createdAt: -1 }).exec()
  return bikes
}

export default {
  getOne,
  getMany,
}
