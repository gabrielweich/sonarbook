import enum


class ErrorCodeEnum(enum.Enum):
    INTERNAL_SERVER_ERROR = "internal-server-error"
    VALIDATION_ERROR = "validation-error"
    NOT_FOUND = "not-found"
    INVALID_CREDENTIALS = "invalid-credentials"
    ALREADY_EXISTS = "already-exists"


class ApplicationError(Exception):
    def __init__(self, code: ErrorCodeEnum, message: str):
        self.code = code
        self.message = message


class UnauthorizedError(ApplicationError):
    pass


class AlreadyExistsError(ApplicationError):
    pass


class NotFoundError(Exception):
    def __init__(self, message: str):
        self.code = ErrorCodeEnum.NOT_FOUND
        self.message = message
