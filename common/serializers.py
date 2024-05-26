from rest_framework import status

class CustomResponse:
    @staticmethod
    def success(data=None, msg='Success', status_code=status.HTTP_200_OK):
        return {'msg': msg, 'status': status_code, 'data': data}

    @staticmethod
    def error(msg='Error', status_code=status.HTTP_400_BAD_REQUEST):
        return {'msg': msg, 'status': status_code, 'data': None}
