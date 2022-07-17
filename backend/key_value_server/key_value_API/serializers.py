from rest_framework import serializers
from .models import KeyValue


# Source: https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
# Supplemented with field validation by me
class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)

            if allowed.issubset(existing):
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            else:
                raise ValueError("None existent desired field.")


class KeyValueSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = KeyValue
        fields = ["key", "value"]

