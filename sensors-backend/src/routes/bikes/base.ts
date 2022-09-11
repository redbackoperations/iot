import { Router } from 'express'
import getRouter from './get-router'

const baseRouter = Router()

baseRouter.use('/', getRouter)

export default baseRouter
