import { model, Schema } from 'mongoose'

interface ISpeed {
  value: number
  reportedAt: Date
  metadata: {
    bikeNumber: string
    sensorName?: string
  }
}

const speedSchema = new Schema<ISpeed>(
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

const speedModel = model<ISpeed>('Speed', speedSchema)

export { speedModel, ISpeed }
