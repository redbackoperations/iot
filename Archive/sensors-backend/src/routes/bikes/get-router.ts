import StatusCodes from 'http-status-codes'
import { Request, Response, Router } from 'express'

import BikeRepo from '../../repos/bike'
import { IBike } from '../../models/bike'

const router = Router()

const { OK, BAD_REQUEST } = StatusCodes

/**
 * Get one bike record
 */
router.get('/bike', (req: Request, res: Response) => {
  const { name, id } = req.query

  BikeRepo.getOne({
    name: name as string,
    _id: id as string,
  })
    .then((bike: IBike) => res.status(OK).json({ bike }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

/**
 * Get multiple bike records
 *
 */
router.get('/bikes', (req: Request, res: Response) => {
  const { name, id } = req.query

  BikeRepo.getMany({
    name: name as string,
    _id: id as string,
  })
    .then((bikes: IBike[]) => res.status(OK).json({ bikes }))
    .catch((error: Error) => res.status(BAD_REQUEST).json({ error }))
})

export default router
