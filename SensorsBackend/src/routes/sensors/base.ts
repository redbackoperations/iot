import { Router } from 'express'
import speedRouter from './speed-router'
import cadenceRouter from './cadence-router'

const baseRouter = Router()

baseRouter.use('/sensors', speedRouter)
baseRouter.use('/sensors', cadenceRouter)

export default baseRouter
