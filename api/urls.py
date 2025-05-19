from django.urls import path
from .views import user_list, hello_api

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('hello/', hello_api, name='hello-api')
]