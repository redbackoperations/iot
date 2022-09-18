const jsonFields = ['metadata', 'bluetoothUUIDs']
const ignoredDBAttributes = ['_id', 'createdAt', 'updatedAt', '__v']
const idFields = ['_id', 'bikeId', 'deviceId']

const isJson = (value: string) => {
  try {
    return JSON.parse(value)
  } catch (e) {
    return false
  }
}

export { jsonFields, ignoredDBAttributes, idFields, isJson }
