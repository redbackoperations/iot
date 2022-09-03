import express from 'express'
import * as dotenv from 'dotenv'
import basicAuth from 'express-basic-auth'
import apiRouter from './routes/api'
import './lib/dbConnection'
import { getUnauthorizedResponse } from './lib/authHelper'

dotenv.config()
const port = process.env.API_PORT || 3000 // default port to listen

const app = express()

// Common middlewares
app.use(express.json())

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

// start the Express server
app.listen(port, () => {
  console.log(`server started at http://localhost:${port}`)
})
