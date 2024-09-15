import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'
import asyncHandler from 'express-async-handler'
import { bikeModel } from '../../models/bike'
import { deviceModel, DeviceType } from '../../models/device'
import { deviceDataModel } from '../../models/device-data'

const router = Router()

const { OK, BAD_REQUEST } = StatusCodes

/**
 * Get total counts for all collections
 */
router.get(
  '/total-count',
  asyncHandler(async (req: Request, res: Response) => {
    try {
      const bikesCount = await bikeModel.countDocuments({}).exec()
      const devicesCount = await deviceModel.countDocuments({}).exec()
      const deviceDataCount = await deviceDataModel.countDocuments({}).exec()

      res.status(OK).json({ bikes: bikesCount, devices: devicesCount, deviceData: deviceDataCount })
    } catch (error: unknown) {
      res.status(BAD_REQUEST).json({ error })
    }
  })
)

/**
 * Get total counts for all collections
 */
router.get(
  '/device-data/total-count',
  asyncHandler(async (req: Request, res: Response) => {
    try {
      const deviceTypes = Object.values(DeviceType)
      const deviceTypesCount: Record<string, number> = {}

      for (const deviceType of deviceTypes) {
        const count = await deviceDataModel.countDocuments({ deviceType }).exec()
        deviceTypesCount[deviceType as string] = count
      }
      deviceTypesCount.total = Object.values(deviceTypesCount).reduce((a, b) => a + b)

      res.status(OK).json(deviceTypesCount)
    } catch (error: unknown) {
      res.status(BAD_REQUEST).json({ error })
    }
  })
)

export default router
