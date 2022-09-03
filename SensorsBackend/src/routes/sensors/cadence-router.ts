import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import cadenceRepo from '../../repos/cadence'
import { ICadence } from '../../models/cadence'
import { DEFAULT_GET_DATA_LIMIT } from '../../lib/constants'

const router = Router()

const { OK, BAD_REQUEST } = StatusCodes

/**
 * Get one cadence sensor data record
 */
//  Sample request: curl --location --request GET 'http://localhost:3000/api/sensors/cadence?bikeNumber=00002&before=2022-10-01T12:41:22.500Z&after=2021-10-01T12:41:22.500Z' \
//  --header 'Authorization: Basic BASIC_AUTH_CREDS_HERE'

router.get('/cadence', (req: Request, res: Response) => {
  const { bikeNumber, before, after } = req.query

  cadenceRepo
    .getOne({
      bikeNumber: bikeNumber as string,
      before: before ? new Date(before as string) : null,
      after: after ? new Date(after as string) : null,
    })
    .then((cadence: ICadence) => res.status(OK).json({ cadence }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

/**
 * Get multiple cadence sensor data records
 *
 */

//  curl --location --request GET 'http://localhost:3000/api/sensors/cadences?bikeNumber=00002&before=2022-10-01T12:41:22.500Z&after=2021-10-01T12:41:22.500Z&limit=2' \
//  --header 'Authorization: Basic BASIC_AUTH_CREDS_HERE'

router.get('/cadences', (req: Request, res: Response) => {
  const { bikeNumber, before, after, limit } = req.query

  cadenceRepo
    .getMany({
      bikeNumber: bikeNumber as string,
      before: before ? new Date(before as string) : null,
      after: after ? new Date(after as string) : null,
      limit: Number(limit) || DEFAULT_GET_DATA_LIMIT,
    })
    .then((cadences: ICadence[]) => res.status(OK).json({ cadences }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

export default router
