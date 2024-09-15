/* eslint-disable max-classes-per-file */
import HttpStatusCodes from 'http-status-codes'

abstract class CustomError extends Error {
  public readonly httpStatus = HttpStatusCodes.BAD_REQUEST

  constructor(msg: string, httpStatus: number) {
    super(msg)
    this.httpStatus = httpStatus
  }
}

class ParamMissingError extends CustomError {
  public static readonly msg = 'One or more of the required parameters was missing.'
  public static readonly httpStatus = HttpStatusCodes.BAD_REQUEST

  constructor() {
    super(ParamMissingError.msg, ParamMissingError.httpStatus)
  }
}

class DocumentNotFoundError extends CustomError {
  public static readonly msg = 'Data Not Found'
  public static readonly httpStatus = HttpStatusCodes.NOT_FOUND

  constructor(modelName?: string) {
    super(
      modelName ? `${modelName} ${DocumentNotFoundError.msg}` : DocumentNotFoundError.msg,
      DocumentNotFoundError.httpStatus
    )
  }
}

export { CustomError, ParamMissingError, DocumentNotFoundError }
