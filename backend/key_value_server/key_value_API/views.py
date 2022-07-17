from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

# Create your views here.


@api_view(["GET"])
@renderer_classes([JSONRenderer])
@parser_classes([])
def server_status(request):
    return Response({"status": "Server is running."})