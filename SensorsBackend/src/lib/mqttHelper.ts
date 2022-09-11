const findBikeNumber = (topicName: string) => topicName.match(/\d+/) && topicName.match(/\d+/)[0]

const deviceNameFromTopic = (topicName: string) => topicName.split('/').pop().toLowerCase()

export { findBikeNumber, deviceNameFromTopic }
