from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'projects'

router = DefaultRouter()
router.register(r'projects', ProjectViewSet,basename='project')
router.register(r'contentprojects', ContentProjectViewSet,basename='contentprojects')

urlpatterns = [
    path('', include(router.urls)),
]