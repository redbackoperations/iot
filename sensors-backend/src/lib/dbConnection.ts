import mongoose, { ConnectOptions } from 'mongoose'
import * as dotenv from 'dotenv'

dotenv.config()

mongoose
  .connect(process.env.MONGODB_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    autoIndex: true,
  } as ConnectOptions)
  .then(() => {
    console.log('Connected to MongoDB!')
  })
  .catch((error) => console.error(error))
