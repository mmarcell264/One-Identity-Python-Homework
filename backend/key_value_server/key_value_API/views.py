from .models import KeyValue
from key_value_API import throttles
from key_value_API import service
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, parser_classes, permission_classes, throttle_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

# Create your views here.


@api_view(["GET"])
@throttle_classes([throttles.GetBurstRateThrottle, throttles.GetSustainedRateThrottle])
@renderer_classes([JSONRenderer])
@parser_classes([])
def server_status(request):
    return Response({"status": "Server is running."})


# Source: https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
#Little bit modifed
class CustomAuthToken(ObtainAuthToken):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    throttle_classes = [throttles.PostBurstRateThrottle, throttles.PostSustainedRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
            })

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@throttle_classes([throttles.PostBurstRateThrottle, throttles.PostSustainedRateThrottle])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def add_key_value(request):
    result = service.request_data_validation(request.data)

    if result["error"]:
        return result["data"]
    else:
        serializer = service.key_value_serialization_or_500(data=result["data"])
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Key-value pair has been successfully created."}, HTTP_201_CREATED)

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@throttle_classes([throttles.GetBurstRateThrottle, throttles.GetSustainedRateThrottle])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
@parser_classes([])
def get_value_by_key(request, key):
    obj = get_object_or_404(KeyValue, key=key)

    serializer = service.key_value_serialization_or_500(obj, fields=('value',))

    return Response(serializer.data)


@api_view(["GET"])
@throttle_classes([throttles.GetBurstRateThrottle, throttles.GetSustainedRateThrottle])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
@parser_classes([])
def get_keys_by_value_prefix(request):
    params = request.query_params

    if "prefix" in params.keys():
        query_set = KeyValue.objects.filter(value__startswith=params["prefix"])

        paginator = PageNumberPagination()
        paginator.page_size = 100
        result_page = paginator.paginate_queryset(query_set, request)

        serializer = service.key_value_serialization_or_500(result_page, fields=('key',), many=True)

        return paginator.get_paginated_response(serializer.data)

    return Response({"error": "Please use the prefix parameter."}, HTTP_400_BAD_REQUEST)

