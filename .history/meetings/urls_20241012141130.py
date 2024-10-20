from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'meetings'


urlpatterns = [
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
]