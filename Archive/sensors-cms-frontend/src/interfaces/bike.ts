interface Bike {
  _id: string
  name: string
  label: string
  description: string
  mqttTopicPrefix: string
  mqttReportTopicSuffix: string
  createdAt: Date
  updatedAt: Date
}

export default Bike
