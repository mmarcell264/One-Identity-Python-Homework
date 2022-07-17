from .serializers import KeyValueSerializer
from key_value_API import service
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.


@api_view(["GET"])
@renderer_classes([JSONRenderer])
@parser_classes([])
def server_status(request):
    return Response({"status": "Server is running."})


@api_view(["POST"])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def add_key_value(request):
    result = service.request_data_validation(request.data)

    if result["error"]:
        return result["data"]
    else:
        serializer = KeyValueSerializer(data=result["data"])
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Key-value pair has been successfully created."}, HTTP_201_CREATED)

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)