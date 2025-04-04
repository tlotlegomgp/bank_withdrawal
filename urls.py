from django.urls import path

from .views import WithdrawView

urlpatterns = [
    path("bank/withdraw/", WithdrawView.as_view()),  # Withdrawal url endpoint
]
