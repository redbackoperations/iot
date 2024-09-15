import { Router } from 'express'
import getRouter from './get-router'
import upsertRouter from './upsert-router'
import deleteRouter from './delete-router'

const baseRouter = Router()

baseRouter.use('/', getRouter)
baseRouter.use('/', upsertRouter)
baseRouter.use('/', deleteRouter)

export default baseRouter
