import { IBasicAuthedRequest } from 'express-basic-auth'

const getUnauthorizedResponse = (req: IBasicAuthedRequest) => {
  const message = req.auth
    ? 'Credentials ' + req.auth.user + ':' + req.auth.password + ' rejected'
    : 'No credentials provided'
  return { error: message }
}

export { getUnauthorizedResponse }
