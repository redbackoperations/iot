import { Router } from 'express'
import bikesRouter from './bikes/base'
import devicesRouter from './devices/base'
import deviceDataRouter from './device-data/base'
import dataAnalyticsRouter from './data-analytics/base'

// Export the base-router
const apiRouter = Router()

// Setup routers
apiRouter.use('/', bikesRouter)
apiRouter.use('/', devicesRouter)
apiRouter.use('/', deviceDataRouter)
apiRouter.use('/', dataAnalyticsRouter)

export default apiRouter
