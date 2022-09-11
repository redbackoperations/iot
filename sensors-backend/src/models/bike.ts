import { model, Schema } from 'mongoose'

interface IBike {
  name: string
  label: string
  description: string
  mqttTopicPrefix: string
  mqttReportTopicSuffix: string
  createdAt: Date
  updatedAt: Date
}

const bikeSchema = new Schema<IBike>(
  {
    name: { type: String },
    label: { type: String },
    description: { type: String },
    mqttTopicPrefix: { type: String },
    mqttReportTopicSuffix: { type: String },
    createdAt: { type: Date },
    updatedAt: { type: Date },
  },
  { timestamps: true }
)

const bikeModel = model<IBike>('Bike', bikeSchema)

export { bikeModel, IBike }
