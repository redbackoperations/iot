import { Router } from 'express'
import deviceDataRouter from './device-data/base'

// Export the base-router
const apiRouter = Router()

// Setup routers
apiRouter.use('/', deviceDataRouter)

export default apiRouter
