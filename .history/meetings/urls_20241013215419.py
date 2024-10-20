from django.urls import path, include
from django.urls import path
from .views import MeetingListCreateView, MeetingDetailView
app_name = 'meetings'


urlpatterns = [
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
]
