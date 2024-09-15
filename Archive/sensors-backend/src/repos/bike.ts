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

/**
 * Create a bike record
 */
const create = async (payload: IBike): Promise<IBike> => {
  return await bikeModel.create(payload)
}

/**
 * Update a bike record
 */
const update = async (id: string, payload: IBike): Promise<IBike> => {
  return await bikeModel.findByIdAndUpdate(id, payload, {
    new: true,
    runValidators: true,
    context: 'query',
  })
}

/**
 * Delete a bike record
 */
const _delete = async (id: string): Promise<IBike> => {
  return await bikeModel.findByIdAndDelete(id)
}

export default {
  getOne,
  getMany,
  create,
  update,
  delete: _delete,
}
