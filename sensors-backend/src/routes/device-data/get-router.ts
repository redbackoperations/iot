import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import deviceDataRepo from '../../repos/device-data'
import { IDeviceData } from '../../models/device-data'
import { DEFAULT_GET_DATA_LIMIT } from '../../lib/constants'
import { DeviceType } from '../../models/device'

const router = Router()

const { OK, BAD_REQUEST } = StatusCodes

/**
 * Get one device data record
 */
//  Sample request: curl --location --request GET 'http://localhost:3000/api/device-data?bikeName=00002&before=2022-10-01T12:41:22.500Z&after=2021-10-01T12:41:22.500Z' \
//  --header 'Authorization: Basic BASIC_AUTH_CREDS_HERE'

router.get('/', (req: Request, res: Response) => {
  const { deviceType, bikeName, before, after } = req.query

  deviceDataRepo
    .getOne({
      deviceType: deviceType as DeviceType,
      bikeName: bikeName as string,
      before: before ? new Date(before as string) : null,
      after: after ? new Date(after as string) : null,
    })
    .then((deviceData: IDeviceData) => res.status(OK).json({ deviceData }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

/**
 * Get multiple device data records
 *
 */

//  curl --location --request GET 'http://localhost:3000/api/device-data/many?bikeName=00002&before=2022-10-01T12:41:22.500Z&after=2021-10-01T12:41:22.500Z&limit=2' \
//  --header 'Authorization: Basic BASIC_AUTH_CREDS_HERE'

router.get('/many', (req: Request, res: Response) => {
  const { deviceType, bikeName, before, after, limit } = req.query

  deviceDataRepo
    .getMany({
      deviceType: deviceType as DeviceType,
      bikeName: bikeName as string,
      before: before ? new Date(before as string) : null,
      after: after ? new Date(after as string) : null,
      limit: Number(limit) || DEFAULT_GET_DATA_LIMIT,
    })
    .then((deviceDatas: IDeviceData[]) => res.status(OK).json({ deviceDatas }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

export default router
