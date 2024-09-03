from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'workreport'
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkReportViewSet

router = DefaultRouter()
router.register(r'workreports', WorkReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('workreports/<int:pk>/approve/', WorkReportViewSet.as_view({'post': 'approve'}), name='workreport-approve'),
]
