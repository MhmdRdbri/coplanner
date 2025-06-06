from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet

app_name = 'ticket'

router = DefaultRouter()
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]