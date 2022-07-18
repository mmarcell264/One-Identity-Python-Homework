from .models import KeyValue
from key_value_API import views
from key_value_API import service
from rest_framework.test import APITestCase
from rest_framework.exceptions import APIException
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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


class TestServerStatus(APITestCase):

    def test_server_is_up(self):
        url = reverse("key_value_API:server_status")
        response = self.client.get(url, format="json")

        self.assertEqual(response.data, {"status": "Server is running."})


class TestCustomAuthToken(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='test')

    def test_not_valid_username_password(self):
        url = reverse("key_value_API:token_auth")

        data = {"username": "test", "password": "password"}

        response= self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_token(self):
        url = reverse("key_value_API:token_auth")

        data = {"username": "test", "password": "test"}

        response= self.client.post(url, data=data, format='json')

        self.assertTrue(response.data['token'])


class TestAddKeyValue(APITestCase):

    def setUp(self):
        key_value = KeyValue(key="window", value="big")
        key_value.save()

        self.user = User.objects.create_user(
            username='test',  password='test')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.token = f"Bearer {self.token}"

    def test_wrong_input_type(self):
        url = reverse("key_value_API:add_key_and_value")

        data_list = [{"key": "trial_key1", "value": "trial_value1"},
                    {"key": "trial_key2", "value": "trial_value2"}]
        data_bare = 10

        response_list = self.client.post(url, data=data_list, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response_list.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_list.data, {"error": "Not valid input."})
        self.assertEqual(KeyValue.objects.count(), 1)

        response_bare = self.client.post(url, data=data_bare, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response_bare.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_bare.data, {"error": "Not valid input."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_too_few_fields(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token,)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Too few input fields."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_too_many_fields(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"a": "a", "b": "b" , "c": "c"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Too many input fields."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_missing_key_field(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"a": "trial_key", "value": "trial_value"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,{"error": "Missing key or value field."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_missing_value_field(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"key": "trial_key", "b": "trial_value"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing key or value field."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_missing_key_value_field(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"a": "trial_key", "b": "trial_value"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Missing key or value field."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_wrong_key_field_type(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"key": 5, "value": "trial_value"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "The key's and value's value should be string."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_wrong_value_field_type(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"key": "trial_key", "value": 5}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "The key's and value's value should be string."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_wrong_key_value_field_type(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"key": 5, "value": 10}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "The key's and value's value should be string."})
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_add_same_key_with_different_value(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"key": "window", "value": "big"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token,)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(KeyValue.objects.count(), 1)

    def test_successful_add(self):
        url = reverse("key_value_API:add_key_and_value")

        data = {"key": "trial_key", "value": "trial_value"}

        response = self.client.post(url, data=data, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"status": "Key-value pair has been successfully created."})
        self.assertEqual(KeyValue.objects.count(), 2)


class TestGetValueByKey(APITestCase):
    def setUp(self):
        key_value = KeyValue(key="window", value="big")
        key_value.save()

        self.user = User.objects.create_user(
            username='test', password='test')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.token = f"Bearer {self.token}"

    def test_key_not_found(self):
        url = reverse("key_value_API:get_value_by_key", kwargs={"key": "trial"})

        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_key_found(self):
        url = reverse("key_value_API:get_value_by_key", kwargs={"key": "window"})

        response = self.client.get(url, format='json', HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.data, {"value": "big"})


class TestGetKeysByValuePrefix(APITestCase):
    def setUp(self):
        KeyValue.objects.create(key="big", value="window")
        KeyValue.objects.create(key="acceptable", value="wicca")
        KeyValue.objects.create(key="aggressive", value="wicks")
        KeyValue.objects.create(key="boring", value="wicky")
        KeyValue.objects.create(key="distinct", value="Widdy")

        self.user = User.objects.create_user(
            username='test', password='test')
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.token = f"Bearer {self.token}"

    def test_missing_prefix_parameter(self):
        url = reverse("key_value_API:get_keys_by_value_prefix")

        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Please use the prefix parameter."})

    def test_with_prefix_parameter(self):
        url = reverse("key_value_API:get_keys_by_value_prefix")

        response = self.client.get(url, {"prefix": 'wi'},format="json", HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.data["count"], 4)
