import { ObjectId } from 'mongodb'
import { model, Schema } from 'mongoose'
import { DeviceType } from './device'

// a type for the MQTT message payload
interface IMQTTDeviceData {
  bikeId?: ObjectId
  deviceId?: ObjectId
  workoutId?: ObjectId
  userId?: ObjectId
  deviceName?: string
  bikeName?: string
  unitName: string
  value: number
  metadata?: object
  reportedAt?: Date
}

// this is a device data model, a typical device data record could be a record of speed/candence/heart rate/power, resistance, incline or windspeed
interface IDeviceData extends IMQTTDeviceData {
  deviceType: DeviceType
  createdAt: Date
  updatedAt: Date
}

const deviceDataSchema = new Schema<IDeviceData>(
  {
    bikeId: { type: ObjectId },
    deviceId: { type: ObjectId },
    workoutId: { type: ObjectId },
    userId: { type: ObjectId },
    deviceType: { type: String, enum: DeviceType },
    deviceName: { type: String },
    bikeName: { type: String },
    unitName: { type: String },
    value: { type: Number },
    metadata: { type: Object },
    // TODO: add more specific metadata attributes later.
    reportedAt: { type: Date, default: Date.now() },
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

const deviceDataModel = model<IDeviceData>('DeviceData', deviceDataSchema)

export { deviceDataModel, IMQTTDeviceData, IDeviceData }
