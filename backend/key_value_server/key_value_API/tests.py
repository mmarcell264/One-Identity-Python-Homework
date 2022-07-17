from key_value_API import service
from rest_framework.test import APITestCase
from rest_framework.exceptions import APIException

# Create your tests here.


class TestKeyValueSerializer(APITestCase):

    def test_baseline_fields(self):
        serializer = service.key_value_serialization_or_500()

        fields = tuple(serializer.fields.keys())

        self.assertTupleEqual(fields, ('key', 'value'))

    def test_only_value_field(self):
        serializer = service.key_value_serialization_or_500(fields=('value',))

        fields = tuple(serializer.fields.keys())

        self.assertTupleEqual(fields, ('value',))

    def test_only_key_field(self):
        serializer = service.key_value_serialization_or_500(fields=('key',))

        fields = tuple(serializer.fields.keys())

        self.assertTupleEqual(fields, ('key',))

    def test_both_field(self):
        serializer = service.key_value_serialization_or_500(fields=('key', 'value'))

        fields = tuple(serializer.fields.keys())

        self.assertTupleEqual(fields, ('key', 'value'))

    def test_none_existing_field(self):

        self.assertRaises(APIException, service.key_value_serialization_or_500, fields=('none_existent',))