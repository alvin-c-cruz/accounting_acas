from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MainAccount, SubAccount, AccountType, AccountClass
from collections import defaultdict


@login_required
def chart_of_accounts(request):
    """
    Display the Chart of Accounts grouped by Account Type in Trial Balance format.
    Shows all accounts with their debit and credit balances.
    For expense accounts, shows 3-level hierarchy: Main Account → Account Class → Sub Accounts
    """
    from decimal import Decimal

    # Get all account types and organize accounts by type
    accounts_by_type = {}
    total_debits = Decimal('0.00')
    total_credits = Decimal('0.00')

    for account_type in AccountType:
        main_accounts = MainAccount.objects.filter(
            account_type=account_type.value,
            is_active=True
        ).prefetch_related('sub_accounts', 'account_classes__sub_accounts')

        if main_accounts.exists():
            accounts_data = []

            for main_account in main_accounts:
                # For EXPENSE accounts, organize by Account Class (3-level hierarchy)
                if account_type == AccountType.EXPENSE:
                    # Get all account classes for this main account
                    account_classes = main_account.account_classes.filter(is_active=True).order_by('code')

                    # Add sub-accounts grouped by account class
                    for account_class in account_classes:
                        # Add account class header
                        accounts_data.append({
                            'type': 'class_header',
                            'account_class': account_class,
                            'main_account': main_account,
                        })

                        # Add sub-accounts under this class
                        for sub_account in account_class.sub_accounts.filter(is_active=True):
                            balance = sub_account.get_balance()
                            normal_balance = sub_account.get_normal_balance()

                            if normal_balance == 'DEBIT':
                                debit = balance if balance > 0 else Decimal('0')
                                credit = abs(balance) if balance < 0 else Decimal('0')
                            else:
                                credit = balance if balance > 0 else Decimal('0')
                                debit = abs(balance) if balance < 0 else Decimal('0')

                            total_debits += debit
                            total_credits += credit

                            accounts_data.append({
                                'type': 'sub_account',
                                'sub_account': sub_account,
                                'main_account': main_account,
                                'account_class': account_class,
                                'debit': debit,
                                'credit': credit,
                            })

                    # Add sub-accounts without account class (if any)
                    unclassified_subs = main_account.sub_accounts.filter(
                        is_active=True,
                        account_class__isnull=True
                    )
                    if unclassified_subs.exists():
                        accounts_data.append({
                            'type': 'class_header',
                            'class_name': 'Unclassified',
                            'main_account': main_account,
                        })
                        for sub_account in unclassified_subs:
                            balance = sub_account.get_balance()
                            normal_balance = sub_account.get_normal_balance()

                            if normal_balance == 'DEBIT':
                                debit = balance if balance > 0 else Decimal('0')
                                credit = abs(balance) if balance < 0 else Decimal('0')
                            else:
                                credit = balance if balance > 0 else Decimal('0')
                                debit = abs(balance) if balance < 0 else Decimal('0')

                            total_debits += debit
                            total_credits += credit

                            accounts_data.append({
                                'type': 'sub_account',
                                'sub_account': sub_account,
                                'main_account': main_account,
                                'debit': debit,
                                'credit': credit,
                            })

                # For non-EXPENSE accounts, use simple 2-level hierarchy
                else:
                    for sub_account in main_account.sub_accounts.filter(is_active=True):
                        balance = sub_account.get_balance()
                        normal_balance = sub_account.get_normal_balance()

                        if normal_balance == 'DEBIT':
                            debit = balance if balance > 0 else Decimal('0')
                            credit = abs(balance) if balance < 0 else Decimal('0')
                        else:
                            credit = balance if balance > 0 else Decimal('0')
                            debit = abs(balance) if balance < 0 else Decimal('0')

                        total_debits += debit
                        total_credits += credit

                        accounts_data.append({
                            'type': 'sub_account',
                            'sub_account': sub_account,
                            'main_account': main_account,
                            'debit': debit,
                            'credit': credit,
                        })

            if accounts_data:
                accounts_by_type[account_type] = accounts_data

    context = {
        'accounts_by_type': accounts_by_type,
        'total_main_accounts': MainAccount.objects.filter(is_active=True).count(),
        'total_sub_accounts': SubAccount.objects.filter(is_active=True).count(),
        'total_debits': total_debits,
        'total_credits': total_credits,
        'is_balanced': abs(total_debits - total_credits) < Decimal('0.01'),
    }

    return render(request, 'accounts/chart_of_accounts.html', context)


@login_required
def account_detail(request, account_id):
    """
    Display detailed information about a specific sub-account including recent transactions.
    """
    from django.shortcuts import get_object_or_404

    sub_account = get_object_or_404(SubAccount, id=account_id)

    # Get recent transaction lines for this account
    recent_transactions = sub_account.transaction_lines.filter(
        journal_entry__is_posted=True
    ).select_related('journal_entry').order_by('-journal_entry__date')[:20]

    context = {
        'sub_account': sub_account,
        'recent_transactions': recent_transactions,
        'balance': sub_account.get_balance(),
    }

    return render(request, 'accounts/account_detail.html', context)
