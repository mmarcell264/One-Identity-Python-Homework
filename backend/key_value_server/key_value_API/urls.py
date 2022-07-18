from django.urls import path
from key_value_API import views

app_name = "key_value_API"

urlpatterns = [
    path("", views.server_status, name="server_status"),
    path('token-auth/', views.CustomAuthToken.as_view(), name="token_auth"),
    path("add/", views.add_key_value, name="add_key_and_value"),
    path("get/<key>/value/", views.get_value_by_key ,name="get_value_by_key"),
    path("get/keys/", views.get_keys_by_value_prefix, name="get_keys_by_value_prefix"),
]
