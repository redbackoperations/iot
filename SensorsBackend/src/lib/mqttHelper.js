const findBikeNumber = (topicName) => topicName.match(/\d+/) && topicName.match(/\d+/)[0]

export { findBikeNumber }
