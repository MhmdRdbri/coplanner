from rest_framework import serializers
from .models import Account, Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'date', 'description']

class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'transactions']