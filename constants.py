from django.db.models import TextChoices

class WithdrawalStatus(TextChoices):
    SUCCESSFUL = "Withdrawal successful."
    FAILED = "Withdrawal failed."
    INSUFFICIENT_FUNDS = "Insufficient funds for withdrawal."
    
    def __str__(self):
        return self.value
