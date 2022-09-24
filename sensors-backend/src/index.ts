import express, { Request, Response, NextFunction } from 'express'
import morgan from 'morgan'
import * as dotenv from 'dotenv'
import basicAuth from 'express-basic-auth'
import cors from 'cors'
import StatusCodes from 'http-status-codes'
import apiRouter from './routes/api'
import './lib/dbConnection'
import { getUnauthorizedResponse } from './lib/authHelper'
import { CustomError } from './lib/httpErrors'
import helmet from 'helmet'

dotenv.config()
const port = process.env.API_PORT || 3000 // default port to listen

const app = express()

app.use(helmet())

// add server logger
app.use(morgan('combined'))

// Common middlewares
app.use(express.json())
app.use(cors())

// define a route handler for the default home page
app.get('/', (req, res) => {
  res.send('The sensor data API server is running now...')
})

// apply a basic auth for all APIs
// TODO: apply a better Auth mechanism if needed later
app.use(
  basicAuth({
    users: { [process.env.BASIC_AUTH_USERNAME]: process.env.BASIC_AUTH_PASSWORD },
    unauthorizedResponse: getUnauthorizedResponse,
  })
)

// add all API routers
app.use('/api', apiRouter)

// eslint-disable-next-line @typescript-eslint/no-unused-vars
app.use((err: Error | CustomError, req: Request, res: Response, _: NextFunction) => {
  // logger.err(err, true)
  const status = err instanceof CustomError ? err.httpStatus : StatusCodes.BAD_REQUEST
  return res.status(status).json({
    error: err.message,
  })
})

// start the Express server
app.listen(port, () => {
  console.log(`server started at http://localhost:${port}`)
})
