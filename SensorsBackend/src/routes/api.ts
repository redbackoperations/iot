import { Router } from 'express'
import sensorsRouter from './sensors/base'

// Export the base-router
const apiRouter = Router()

// Setup routers
apiRouter.use('/', sensorsRouter)

export default apiRouter
