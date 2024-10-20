from django.db import models
from django.conf import settings

class Account(models.Model):
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('salary', 'Salary'),
    ]

    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE, default=1)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    amount = models.IntegerField(max_digits=15)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    file = models.FileField(upload_to='invoices/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.transaction_type in ['income',]:
            self.account.balance += self.amount
        elif self.transaction_type in ['expense', 'salary']:
            self.account.balance -= self.amount
        self.account.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.transaction_type in ['income',]:
            self.account.balance -= self.amount
        elif self.transaction_type in ['expense','salary']:
            self.account.balance += self.amount
        self.account.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
