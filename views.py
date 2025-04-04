import boto3
import logging
import json
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .contants import WithdrawalStatus
from .models import BankAccount
from .serializers import WithdrawalSerializer

# Configure logging
logger = logging.getLogger(__name__)

# Create SNS client instance
sns_client = boto3.client("sns", region_name=settings.AWS_REGION)


def get_withdrawal_event_data(account_id: int, amount: Decimal, status: str) -> str:
    """Returns a JSON string representing the withdrawal event."""
    event_data = {
        "accountId": account_id,
        "amount": str(amount),
        "status": status,
    }
    return json.dumps(event_data)


# API View for Withdrawal
class WithdrawView(APIView):
    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        amount = serializer.validated_data["amount"]
        account_id = serializer.validated_data["accountID"]

        # Will throw 404 error if BankAccount with id is not found
        account = get_object_or_404(BankAccount, id=account_id)

        # We dont have check if balance is null
        # We can assume balanace cannot be null in the model and is defaulted to 0 on entry creation
        if account.balance < amount:
            return Response(
                {"error": WithdrawalStatus.INSUFFICIENT_FUNDS},
                status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info(f"Withdrawal attempt for Account ID {account_id}, Amount: {amount}")
        try:
            with transaction.atomic():
                # Deduct amount
                account.balance -= amount
                account.save()

                # Publish to SNS
                event_data = get_withdrawal_event_data(
                    account_id, amount, WithdrawalStatus.SUCCESSFUL.name
                )
                sns_topic_arn = settings.AWS_SNS_TOPIC_ARN
                try:
                    response = sns_client.publish(
                        TopicArn=sns_topic_arn, Message=event_data
                    )
                    logger.info(
                        f"SNS Message Published for Account {account_id}: {response}"
                    )
                except Exception as sns_error:
                    logger.error(f"SNS publishing failed: {sns_error}")
                    raise ValueError(
                        "SNS notification failed"
                    )  # Causes transaction rollback

                return Response(
                    {"message": WithdrawalStatus.SUCCESSFUL}, status=status.HTTP_200_OK
                )

        except ValueError as ve:
            return Response(
                {"error": str(ve)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            logger.critical(
                f"Error processing withdrawal for Account ID {account_id}: {e}"
            )
            return Response(
                {"error": WithdrawalStatus.FAILED},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
