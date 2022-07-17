from django.urls import path
from key_value_API import views

app_name = "key_value_API"

urlpatterns = [
    path("", views.server_status, name="server_status"),
    path("add/", views.add_key_value, name="add_key_and_value"),
]
