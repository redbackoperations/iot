import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import DeviceRepo from '../../repos/device'
import { IDevice } from '../../models/device'
import { ParamMissingError, DocumentNotFoundError } from '../../lib/httpErrors'

interface DeviceRequest<T> extends Request {
  body: { device: T }
  params: { id: string }
}

const router = Router()

const { OK, BAD_REQUEST, NOT_FOUND } = StatusCodes

/**
 * Create one device record
 */
router.post('/devices', (req: DeviceRequest<IDevice>, res: Response) => {
  const { device } = req.body
  if (!device) {
    throw new ParamMissingError()
  }

  DeviceRepo.create(device)
    .then((data: IDevice) => res.status(OK).json({ device: data }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error: error.message }))
})

/**
 * Update one device record
 */
router.put('/devices/:id', (req: DeviceRequest<IDevice>, res: Response) => {
  const { device } = req.body
  const { id } = req.params
  if (!id || !device) {
    throw new ParamMissingError()
  }

  DeviceRepo.update(id, device)
    .then((data: IDevice) => {
      if (!data) throw new DocumentNotFoundError('Bike')
      res.status(OK).json({ device: data })
    })
    .catch((error: DocumentNotFoundError | Error) => {
      res
        .status(error instanceof DocumentNotFoundError ? NOT_FOUND : BAD_REQUEST)
        .json({ error: error.message })
    })
})

export default router
