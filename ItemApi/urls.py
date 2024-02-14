from django.contrib import admin
from django.urls import path, include
from .views import ItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('items', ItemViewSet)

urlpatterns = router.urls