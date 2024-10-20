from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
from .views import TimeSheetStartView, TimeSheetPauseResumeView, TimeSheetStopView, TimeSheetListView

app_name = 'timesheet'

urlpatterns = [
    path('start/', TimeSheetStartView.as_view(), name='timesheet-start'),
    path('pause-resume/', TimeSheetPauseResumeView.as_view(), name='timesheet-pause-resume'),
    path('stop/', TimeSheetStopView.as_view(), name='timesheet-stop'),
    path('list/', TimeSheetListView.as_view(), name='timesheet-list'),
]