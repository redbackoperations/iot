import axios from 'axios'

const axiosClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
  //   TODO: add safer AUTH mechanism later
  auth: {
    username: process.env.REACT_APP_API_USERNAME as string,
    password: process.env.REACT_APP_API_PASSWORD as string,
  },
})

export default axiosClient
