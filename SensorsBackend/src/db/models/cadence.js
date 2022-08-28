import mongoose from 'mongoose'

const CadenceSchema = new mongoose.Schema(
  {
    value: { type: Number, min: 0.0 },
    reportedAt: { type: Date, default: Date.now },
    metadata: {
      bikeNumber: String,
      sensorName: String,
    },
    // TODO: add more assoicated attributes later. Eg. user_id, profile_id and other metadata
  },
  {
    timeseries: {
      timeField: 'reportedAt',
      metaField: 'metadata',
      granularity: 'seconds',
    },
  }
)

const Cadence = mongoose.model('Cadence', CadenceSchema)

export default Cadence
