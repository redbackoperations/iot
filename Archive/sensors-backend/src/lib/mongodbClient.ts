import { MongoClient } from 'mongodb'
import * as dotenv from 'dotenv'

dotenv.config()

// Replace the uri string with your connection string.
const uri = process.env.MONGODB_URL

// Create a new MongoClient
const client = new MongoClient(uri)
const run = async () => {
  try {
    // Connect the client to the server (optional starting in v4.7)
    await client.connect()
    // Establish and verify connection
    await client.db('admin').command({ ping: 1 })
    console.log('Connected successfully to server')
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close()
  }
}

run().catch(console.dir)
