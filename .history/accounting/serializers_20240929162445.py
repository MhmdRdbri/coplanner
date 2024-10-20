from rest_framework import serializers
from .models import Account, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'date', 'description','file']


    def get_formatted_amount(self, obj):
        # Convert the amount to an integer and format it with dots
        amount = int(obj.amount)  # Assuming you don't want any decimals
        return "{:,.0f}".format(amount).replace(",", ".")

class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'balance', 'transactions']

    def get_formatted_amount(self, obj):
        # Convert the amount to an integer and format it with dots
        amount = int(obj.amount)  # Assuming you don't want any decimals
        return "{:,.0f}".format(amount).replace(",", ".")  # Replace commas with dots


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'