from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('self/profile/', ProfileUserUpdateView.as_view(), name='profile-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    ]
