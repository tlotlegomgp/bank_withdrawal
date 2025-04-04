from rest_framework import serializers

class WithdrawalSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(
        decimal_places=2,
        min_value=0.01, # Prevents negative or zero withdrawals
    )
