from .views import UserView
from django.urls import path

urlpatterns = [
    path('users/', UserView.as_view(), name='user-list')
]
