from fastapi import status

from app.schemas.errors import ErrorResponse


def error_response(description: str) -> dict:
    return {
        'model': ErrorResponse,
        'description': description,
    }


COMMON_ERROR_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: error_response('Bad request'),
    status.HTTP_401_UNAUTHORIZED: error_response('Unauthorized'),
    status.HTTP_403_FORBIDDEN: error_response('Forbidden'),
    status.HTTP_404_NOT_FOUND: error_response('Not found'),
    status.HTTP_409_CONFLICT: error_response('Conflict'),
    status.HTTP_429_TOO_MANY_REQUESTS: error_response('Rate limit exceeded'),
    status.HTTP_422_UNPROCESSABLE_ENTITY: error_response('Validation error'),
}

AUTH_ERROR_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: error_response('Invalid auth request'),
    status.HTTP_401_UNAUTHORIZED: error_response('Invalid credentials or token'),
    status.HTTP_403_FORBIDDEN: error_response('Account is not confirmed'),
    status.HTTP_409_CONFLICT: error_response('User already exists'),
    status.HTTP_429_TOO_MANY_REQUESTS: error_response('Rate limit exceeded'),
    status.HTTP_422_UNPROCESSABLE_ENTITY: error_response('Validation error'),
}
