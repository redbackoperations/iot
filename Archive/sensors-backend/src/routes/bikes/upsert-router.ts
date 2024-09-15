import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import BikeRepo from '../../repos/bike'
import { IBike } from '../../models/bike'
import { ParamMissingError, DocumentNotFoundError } from '../../lib/httpErrors'

interface BikeRequest<T> extends Request {
  body: { bike: T }
  params: { id: string }
}

const router = Router()

const { OK, BAD_REQUEST, NOT_FOUND } = StatusCodes

/**
 * Create one bike record
 */
router.post('/bikes', (req: BikeRequest<IBike>, res: Response) => {
  const { bike } = req.body
  if (!bike) {
    throw new ParamMissingError()
  }

  BikeRepo.create(bike)
    .then((data: IBike) => res.status(OK).json({ bike: data }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error: error.message }))
})

/**
 * Update one bike record
 */
router.put('/bikes/:id', (req: BikeRequest<IBike>, res: Response) => {
  const { bike } = req.body
  const { id } = req.params
  if (!id || !bike) {
    throw new ParamMissingError()
  }

  BikeRepo.update(id, bike)
    .then((data: IBike) => {
      if (!data) throw new DocumentNotFoundError('Bike')
      res.status(OK).json({ bike: data })
    })
    .catch((error: DocumentNotFoundError | Error) => {
      res
        .status(error instanceof DocumentNotFoundError ? NOT_FOUND : BAD_REQUEST)
        .json({ error: error.message })
    })
})

export default router
