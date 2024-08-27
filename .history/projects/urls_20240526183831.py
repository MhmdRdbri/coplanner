from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'projects'

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'my-projects', MyProjectsViewSet, basename='my-projects')

urlpatterns = [
    path('', include(router.urls)),
]