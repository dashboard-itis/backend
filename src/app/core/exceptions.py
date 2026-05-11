from fastapi import status


class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = 'internal_error'
    message = 'Internal server error'

    def __init__(
        self,
        message: str | None = None,
        details: dict | list | None = None,
    ):
        self.message = message or self.message
        self.details = details


class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = 'bad_request'
    message = 'Bad request'


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = 'unauthorized'
    message = 'Unauthorized'


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = 'forbidden'
    message = 'Forbidden'


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = 'not_found'
    message = 'Resource not found'


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = 'conflict'
    message = 'Resource conflict'


class AccountNotConfirmedError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = 'account_not_confirmed'
    message = 'Account is not confirmed'


class InvalidConfirmationCodeError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = 'invalid_confirmation_code'
    message = 'Invalid or expired confirmation code'
