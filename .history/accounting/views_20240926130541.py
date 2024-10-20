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





api_view(['GET'])
def income_transactions(request):
    incomes = Transaction.objects.filter(transaction_type='income')
    serializer = TransactionSerializer(incomes, many=True)
    return Response(serializer.data)

# 2. List of Outcome Transactions (Expenses/Salary)
@api_view(['GET'])
def outcome_transactions(request):
    outcomes = Transaction.objects.filter(Q(transaction_type='expense') | Q(transaction_type='salary'))
    serializer = TransactionSerializer(outcomes, many=True)
    return Response(serializer.data)

# 3. Final Account Amount
@api_view(['GET'])
def final_account_amount(request):
    total_balance = Account.objects.aggregate(total=Sum('balance'))['total']
    return Response({"total_balance": total_balance})

# 4. Transactions Grouped by 5-Day Periods
@api_view(['GET'])
def transactions_by_5days(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=30)  # Adjust to how far back you want to go (e.g., 30 days)
    
    periods = []
    while start_date <= today:
        end_date = start_date + timedelta(days=5)
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])
        serializer = TransactionSerializer(transactions, many=True)
        periods.append({
            'start_date': start_date,
            'end_date': end_date,
            'transactions': serializer.data
        })
        start_date = end_date
    
    return Response(periods)