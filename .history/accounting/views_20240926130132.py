from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from account.permissions import HasSpecialAccessPermission, IsAdminOrReadOnly
from rest_framework import generics

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [HasSpecialAccessPermission]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [HasSpecialAccessPermission]

class SalaryListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [HasSpecialAccessPermission]

    def get_queryset(self):
        return Transaction.objects.filter(transaction_type='salary')