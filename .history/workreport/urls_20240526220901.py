from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'workreport'

router = DefaultRouter()
router.register(r'workreports', WorkReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]