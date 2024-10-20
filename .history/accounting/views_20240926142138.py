from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from account.permissions import HasSpecialAccessPermission, IsAdminOrReadOnly
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Q

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



@api_view(['GET'])
@permission_classes([HasSpecialAccessPermission])
def accounting_overview(request):
    # 1. Income Transactions
    incomes = Transaction.objects.filter(transaction_type='income')
    income_serializer = TransactionSerializer(incomes, many=True)

    # 2. Outcome Transactions (Expenses/Salary)
    outcomes = Transaction.objects.filter(Q(transaction_type='expense') | Q(transaction_type='salary'))
    outcome_serializer = TransactionSerializer(outcomes, many=True)

    # 3. Final Account Amount
    total_balance = Account.objects.aggregate(total=Sum('balance'))['total']

    # 4. Transactions Grouped by 5-Day Periods
    today = timezone.now().date()
    start_date = today - timedelta(days=30)  # Adjust for desired range
    periods = []
    
    while start_date <= today:
        end_date = start_date + timedelta(days=5)
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])
        transaction_serializer = TransactionSerializer(transactions, many=True)
        periods.append({
            'start_date': start_date,
            'end_date': end_date,
            'transactions': transaction_serializer.data
        })
        start_date = end_date

    # 5. Combine all data into a single response
    response_data = {
        'income_transactions': income_serializer.data,
        'outcome_transactions': outcome_serializer.data,
        'total_account_balance': total_balance,
        'transactions_grouped_by_5days': periods
    }

    return Response(response_data)