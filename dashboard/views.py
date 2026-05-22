from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from accounts.models import MainAccount, AccountType
from transactions.models import TransactionLine
from datetime import datetime, timedelta
from decimal import Decimal


@login_required
def dashboard_view(request):
    """
    Main dashboard view showing summary statistics and recent transactions.
    """
    # Calculate total assets
    assets = MainAccount.objects.filter(
        account_type=AccountType.ASSET,
        is_active=True
    )
    total_assets = sum(account.get_balance() for account in assets)

    # Calculate total liabilities
    liabilities = MainAccount.objects.filter(
        account_type=AccountType.LIABILITY,
        is_active=True
    )
    total_liabilities = sum(account.get_balance() for account in liabilities)

    # Calculate equity (including net income)
    equity_accounts = MainAccount.objects.filter(
        account_type=AccountType.EQUITY,
        is_active=True
    )
    total_equity = sum(account.get_balance() for account in equity_accounts)

    # Calculate net income and add to equity
    revenues = MainAccount.objects.filter(
        account_type=AccountType.REVENUE,
        is_active=True
    )
    expenses = MainAccount.objects.filter(
        account_type=AccountType.EXPENSE,
        is_active=True
    )
    total_revenue = sum(account.get_balance() for account in revenues)
    total_expenses = sum(account.get_balance() for account in expenses)
    net_income = total_revenue - total_expenses
    equity = total_equity + net_income

    # Calculate monthly revenue (current month)
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_revenue = Decimal('0')
    for revenue_account in revenues:
        for sub_account in revenue_account.sub_accounts.filter(is_active=True):
            # Get credit transactions for this month (revenues are credits)
            month_credits = TransactionLine.objects.filter(
                sub_account=sub_account,
                journal_entry__is_posted=True,
                journal_entry__date__gte=current_month_start.date()
            ).aggregate(total=models.Sum('credit'))['total'] or Decimal('0')

            month_debits = TransactionLine.objects.filter(
                sub_account=sub_account,
                journal_entry__is_posted=True,
                journal_entry__date__gte=current_month_start.date()
            ).aggregate(total=models.Sum('debit'))['total'] or Decimal('0')

            monthly_revenue += (month_credits - month_debits)

    context = {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'equity': equity,
        'monthly_revenue': monthly_revenue,
        'recent_transactions': [],
    }

    return render(request, 'dashboard/index.html', context)
