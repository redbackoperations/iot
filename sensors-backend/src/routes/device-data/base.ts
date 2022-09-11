import { Router } from 'express'
import getRouter from './get-router'

const baseRouter = Router()

baseRouter.use('/device-data', getRouter)

export default baseRouter
