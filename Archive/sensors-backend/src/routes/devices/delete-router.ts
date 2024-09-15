import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import DeviceRepo from '../../repos/device'
import { IDevice } from '../../models/device'
import { ParamMissingError, DocumentNotFoundError } from '../../lib/httpErrors'

const router = Router()

const { OK, BAD_REQUEST, NOT_FOUND } = StatusCodes

/**
 * Delete one device record
 */
router.delete('/devices/:id', (req: Request, res: Response) => {
  const { id } = req.params
  if (!id) {
    throw new ParamMissingError()
  }

  DeviceRepo.delete(id)
    .then((device: IDevice) => {
      if (!device) throw new DocumentNotFoundError('Bike')
      res.status(OK).json({ device })
    })
    .catch((error: DocumentNotFoundError | Error) => {
      res
        .status(error instanceof DocumentNotFoundError ? NOT_FOUND : BAD_REQUEST)
        .json({ error: error.message })
    })
})

export default router
