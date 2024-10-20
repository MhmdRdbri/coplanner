from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'accounting'

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('salaries/', SalaryListView.as_view(), name='salary-list'),
    path('accounting-overview/', accounting_overview, name='accounting-overview'),
]
