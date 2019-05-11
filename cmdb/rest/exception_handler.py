from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    print(dir(exc))

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['message'] = response.data['detail']    #增加message这个key
        del response.data['detail']
        # response.data['message'] ='方法不对'    #增加message这个key
    else:
        data = {'status_code': 500, 'message': str(exc)}
        response = Response(data, status=500)
    return response
