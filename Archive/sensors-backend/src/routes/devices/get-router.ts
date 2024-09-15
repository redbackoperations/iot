import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import DeviceRepo from '../../repos/device'
import { IDevice } from '../../models/device'

const router = Router()

const { OK, BAD_REQUEST } = StatusCodes

/**
 * Get one device record
 */
router.get('/device', (req: Request, res: Response) => {
  const { name, id, macAddress } = req.query

  DeviceRepo.getOne({
    name: name as string,
    _id: id as string,
    macAddress: macAddress as string,
  })
    .then((device: IDevice) => res.status(OK).json({ device }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

/**
 * Get multiple device records
 *
 */
router.get('/devices', (req: Request, res: Response) => {
  const { deviceType, mqttTopicDeviceName } = req.query

  DeviceRepo.getMany({
    deviceType: deviceType as string,
    mqttTopicDeviceName: mqttTopicDeviceName as string,
  })
    .then((devices: IDevice[]) => res.status(OK).json({ devices }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

export default router
