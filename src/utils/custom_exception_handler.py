import traceback

from rest_framework.response import Response
from rest_framework.views import exception_handler


def is_registered(exception):
    try:
        return exception.is_an_error_response
    except AttributeError:
        return False


def process_exception(exception, context):
    response = exception_handler(exception, context)
    if is_registered(exception):
        status = exception.status_code
        exception_dict = exception.to_dict()
        traceback.print_exc()
        return Response(data=exception_dict, status=status)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {'errors': []}

        for key, value in response.data.items():
            error = {'field': key, 'message': value}
            customized_response['errors'].append(error)

        response.data = customized_response

    return response
