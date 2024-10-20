from rest_framework import serializers
from .models import Account, Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'date', 'description','file']

class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'transactions']

    def get_formatted_amount(self, obj):
        locale.setlocale(locale.LC_ALL, '')  # Use system's locale settings
        return locale.format_string('%.0f', obj.amount, grouping=True)


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'