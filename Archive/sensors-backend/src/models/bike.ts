import { model, Schema } from 'mongoose'
import uniqueValidator from 'mongoose-unique-validator'

interface IBike {
  _id: Schema.Types.ObjectId
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
    name: { type: String, required: true, unique: true },
    label: { type: String },
    description: { type: String },
    mqttTopicPrefix: { type: String, required: true },
    mqttReportTopicSuffix: { type: String, required: true },
    createdAt: { type: Date },
    updatedAt: { type: Date },
  },
  { timestamps: true }
)
bikeSchema.plugin(uniqueValidator)

const bikeModel = model<IBike>('Bike', bikeSchema)

export { bikeModel, IBike, bikeSchema }
