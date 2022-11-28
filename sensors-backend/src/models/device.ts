import { model, Schema } from 'mongoose'
import uniqueValidator from 'mongoose-unique-validator'
import idValidator from 'mongoose-id-validator'
import './bike'

enum DeviceType {
  speed = 'speed',
  cadence = 'cadence',
  power = 'power',
  heartRate = 'heartrate',
  resistance = 'resistance',
  incline = 'incline',
  fan = 'fan',
}

enum DeviceTypeUnitNames {
  speed = 'm/s',
  cadence = 'RPM',
  power = 'W',
  heartRate = 'BPM',
  resistance = 'percentage',
  incline = 'degree',
  fan = 'percentage',
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
  _id: Schema.Types.ObjectId
  bikeId: Schema.Types.ObjectId
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
    bikeId: { type: Schema.Types.ObjectId, ref: 'Bike', required: false },
    name: { type: String, required: true, unique: true },
    label: { type: String },
    description: { type: String },
    deviceType: { type: String, enum: DeviceType, required: true, index: true },
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
deviceSchema.plugin(idValidator)
deviceSchema.plugin(uniqueValidator)

const deviceModel = model<IDevice>('Device', deviceSchema)

export { deviceModel, ICharacteristic, IService, IDevice, DeviceType, DeviceTypeUnitNames }
