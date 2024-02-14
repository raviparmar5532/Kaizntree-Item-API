from django.urls import path, include

urlpatterns = [
    #Item API
    path('api/', include('ItemApi.urls')),

    #User and Token API
    path('api/', include('UserApi.urls')),
]