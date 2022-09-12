import { Router } from 'express'
import bikesRouter from './bikes/base'
import devicesRouter from './devices/base'
import deviceDataRouter from './device-data/base'

// Export the base-router
const apiRouter = Router()

// Setup routers
apiRouter.use('/', bikesRouter)
apiRouter.use('/', devicesRouter)
apiRouter.use('/', deviceDataRouter)

export default apiRouter
