import { model, Schema } from 'mongoose'
import { DeviceType } from './device'
import idValidator from 'mongoose-id-validator'
import './bike'
import './device'

// a type for the MQTT message payload
interface IMQTTDeviceData {
  _id: Schema.Types.ObjectId
  bikeId?: Schema.Types.ObjectId
  deviceId?: Schema.Types.ObjectId
  workoutId?: Schema.Types.ObjectId
  userId?: Schema.Types.ObjectId
  deviceName?: string
  bikeName?: string
  unitName: string
  value: number
  metadata?: object
  reportedAt?: Date
  timestamp?: Date
}

// this is a device data model, a typical device data record could be a record of speed/candence/heart rate/power, resistance, incline or windspeed
interface IDeviceData extends IMQTTDeviceData {
  deviceType: DeviceType
  createdAt: Date
  updatedAt: Date
}

const deviceDataSchema = new Schema<IDeviceData>(
  {
    bikeId: { type: Schema.Types.ObjectId, ref: 'Bike' },
    deviceId: { type: Schema.Types.ObjectId, ref: 'Device' },
    workoutId: { type: Schema.Types.ObjectId },
    userId: { type: Schema.Types.ObjectId },
    deviceType: { type: String, enum: DeviceType, required: true, index: true },
    deviceName: { type: String },
    bikeName: { type: String },
    unitName: { type: String, required: true },
    value: { type: Number, required: true },
    metadata: { type: Object },
    // TODO: add more specific metadata attributes later.
    reportedAt: { type: Date, default: Date.now(), required: true },
    createdAt: { type: Date },
    updatedAt: { type: Date },
  },
  {
    collection: 'device_data',
    timestamps: true,
    timeseries: {
      timeField: 'reportedAt',
      metaField: 'metadata',
      granularity: 'seconds',
    },
  }
)
deviceDataSchema.plugin(idValidator)

const deviceDataModel = model<IDeviceData>('DeviceData', deviceDataSchema)

export { deviceDataModel, IMQTTDeviceData, IDeviceData }
