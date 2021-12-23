from drf_yasg.utils import swagger_auto_schema
from requests import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import SkiInputSerializer
from api.utils import get_order, extract_ski_data, make_order


@swagger_auto_schema(methods=['get'], request_body=SkiInputSerializer)
@api_view(['GET'])
def ski_rent(request):
    serializer = SkiInputSerializer(data=request.query_params)
    if serializer.is_valid():
        data = serializer.data
        try:
            order = get_order(number=data['id'], passenger_id=data['last_name'])
        except (HTTPError, Exception):
            # HTTPStatusError - исключения, связанные с проблемами на удаленном сервере (4**, 5**)
            # Exception - иные исключения, напр., отсутствует выход Интернет
            # Логгирование, sentry, etc.
            response_data = {
                'error': {
                    'code': 'cannot.get.order',
                    'message': 'Не удалось получить бронь. Пожалуйста, обновите страницу и попробуйте снова.',
                },
                'shoppingCart': None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        ski_data = extract_ski_data(order)
        try:
            make_order(ski_data)
        except (HTTPError, Exception):
            # HTTPStatusError - исключения, связанные с проблемами на удаленном сервере (4xx, 5xx)
            # Exception - иные исключения, напр., отсутствует выход Интернет
            # Логгирование, sentry, etc.
            response_data = {
                'error': {
                    'code': 'conversation.not.found',
                    'message': 'Давайте начнем новый поиск и обновим результаты.',
                },
                'shoppingCart': None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "shoppingCart": {}
        })
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
