from django.db import models
from .waste_collection_record import WasteCollectionRecord
from .user import User


PAYMENT_TYPE = (
    ("credit", "credit"),
    ("debit", "debit"),
)

class Wallet(models.Model):
    order_id=models.CharField(max_length=25)
    payment_id=models.CharField(max_length=25)
    transaction_date = models.DateTimeField(auto_now_add=True)
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')],default = 'credit')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    credit_transactions = models.PositiveIntegerField(default=0)
    debit_transactions = models.PositiveIntegerField(default=0)


    def __str__(self):
        return str(self.order_id)
    