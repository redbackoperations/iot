const findBikeNumber = (topicName: string) => topicName.match(/\d+/) && topicName.match(/\d+/)[0]

export { findBikeNumber }
