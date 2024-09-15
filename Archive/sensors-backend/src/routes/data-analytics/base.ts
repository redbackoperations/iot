import { Router } from 'express'
import getRouter from './get-router'

const baseRouter = Router()

baseRouter.use('/data-analytics', getRouter)
export default baseRouter
