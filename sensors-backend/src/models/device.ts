import { ObjectId } from 'mongodb'
import { model, Schema } from 'mongoose'
import uniqueValidator from 'mongoose-unique-validator'

enum DeviceType {
  speed = 'speed',
  cadence = 'cadence',
  power = 'power',
  heartRate = 'heart-rate',
  resistance = 'resistance',
  incline = 'incline',
  headWind = 'head-wind',
}

// define Bluetooth Service and Characteristic types here
interface ICharacteristic {
  name: string
  uuid: string
}

interface IService extends ICharacteristic {
  characteristics: ICharacteristic[]
}

// this is a bike device model, a device could be a speed/candence/heart rate/power sensor, kickr trainer, kickr climb or headwind
interface IDevice {
  bikeId: ObjectId
  name: string
  label: string
  description: string
  deviceType: DeviceType
  unitName: string
  mqttTopicDeviceName: string
  macAddress: string
  bluetoothName: string
  bluetoothUUIDs: IService[]
  metadata: object
  createdAt: Date
  updatedAt: Date
}

const characteristicSchema = new Schema<ICharacteristic>({
  name: { type: String },
  uuid: { type: String },
})

const serviceSchema = new Schema<IService>({
  name: { type: String },
  uuid: { type: String },
  characteristics: [characteristicSchema],
})

const deviceSchema = new Schema<IDevice>(
  {
    bikeId: { type: ObjectId },
    name: { type: String, required: true, unique: true },
    label: { type: String },
    description: { type: String },
    deviceType: { type: String, enum: DeviceType, required: true },
    unitName: { type: String, required: true },
    mqttTopicDeviceName: { type: String, required: true },
    bluetoothName: { type: String },
    bluetoothUUIDs: { type: [serviceSchema] },
    macAddress: { type: String },
    // TODO: add more specific metadata attributes later.
    metadata: { type: Object },
    createdAt: { type: Date },
    updatedAt: { type: Date },
  },
  { timestamps: true }
)
deviceSchema.plugin(uniqueValidator)

const deviceModel = model<IDevice>('Device', deviceSchema)

export { deviceModel, ICharacteristic, IService, IDevice, DeviceType }
