from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def request_data_validation(data):
    result = {"error": True}

    if not isinstance(data, dict):
        result["data"] = Response({"error": "Not valid input."}, HTTP_400_BAD_REQUEST)
    elif len(data) > 2:
        result["data"] = Response({"error": "Too many input fields."}, HTTP_400_BAD_REQUEST)
    elif len(data) < 2:
        result["data"] = Response({"error": "Too few input fields."}, HTTP_400_BAD_REQUEST)
    else:
        key = data.get("key")
        value = data.get("value")
        if (key is None) or (value is None):
            result["data"] = Response({"error": "Missing key or value field."}, HTTP_400_BAD_REQUEST)
        else:
            if not isinstance(key, str) or not isinstance(value, str):
                result["data"] = Response({"error": "The key's and value's value should be string."}, HTTP_400_BAD_REQUEST)
            else:
                result["error"] = False
                result["data"] = data

    return result
