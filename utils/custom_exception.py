from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from exceptions.custom_apiexception_class import CustomAPIException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Default custom response data
    custom_response_data = {
        "statusCode": response.status_code if response else 500,
        "message": str(exc),
        "error": response.status_text if response else "Internal Server Error",
        "data": None
    }

    # Specific handling for ValidationError
    if isinstance(exc, ValidationError) and response is not None:
        error_messages = []
        for key, value in response.data.items():
            if isinstance(value, list):
                error_messages.extend(value)
        custom_response_data['message'] = " ".join(error_messages)

    # Include additional data for CustomAPIException
    if isinstance(exc, CustomAPIException):
        custom_response_data['data'] = exc.data

    # Update response data
    if response is not None:
        response.data = custom_response_data

    return response
