import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import BikeRepo from '../../repos/bike'
import { IBike } from '../../models/bike'
import { ParamMissingError, DocumentNotFoundError } from '../../lib/httpErrors'

const router = Router()

const { OK, BAD_REQUEST, NOT_FOUND } = StatusCodes

/**
 * Delete one bike record
 */
router.delete('/bikes/:id', (req: Request, res: Response) => {
  const { id } = req.params
  if (!id) {
    throw new ParamMissingError()
  }

  BikeRepo.delete(id)
    .then((bike: IBike) => {
      if (!bike) throw new DocumentNotFoundError('Bike')
      res.status(OK).json({ bike })
    })
    .catch((error: DocumentNotFoundError | Error) => {
      res
        .status(error instanceof DocumentNotFoundError ? NOT_FOUND : BAD_REQUEST)
        .json({ error: error.message })
    })
})

export default router
