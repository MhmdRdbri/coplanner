from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path
from .views import TimesheetViewSet

app_name = 'timesheet'
timesheet_viewset = TimesheetViewSet.as_view({
    'post': 'start',
    'patch': 'pause',
    'put': 'resume',
    'delete': 'stop',
    'get': 'list',
})

urlpatterns = [
    path('start/', TimesheetViewSet.as_view({'post': 'start'}), name='start_timesheet'),
    path('pause/', TimesheetViewSet.as_view({'patch': 'pause'}), name='pause_timesheet'),
    path('resume/', TimesheetViewSet.as_view({'put': 'resume'}), name='resume_timesheet'),
    path('stop/', TimesheetViewSet.as_view({'delete': 'stop'}), name='stop_timesheet'),
    path('list/', TimesheetViewSet.as_view({'get': 'list'}), name='list_timesheets'),
    path('list_for_admin/', TimesheetViewSet.as_view({'get': 'list_for_admin'}), name='list_timesheets_for_admin'),
]
