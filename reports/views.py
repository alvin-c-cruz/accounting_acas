from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import MainAccount, SubAccount, AccountType
from transactions.models import JournalEntry
from decimal import Decimal


@login_required
def reports_index(request):
    """Main reports page with links to all available reports"""
    context = {
        'total_posted_entries': JournalEntry.objects.filter(is_posted=True).count(),
    }
    return render(request, 'reports/index.html', context)


@login_required
def balance_sheet(request):
    """
    Balance Sheet Report
    Shows: Assets = Liabilities + Equity
    Note: Net income from revenue/expense accounts is automatically included in equity
    """
    # Get all asset accounts
    assets = MainAccount.objects.filter(
        account_type=AccountType.ASSET,
        is_active=True
    ).prefetch_related('sub_accounts')

    # Get all liability accounts
    liabilities = MainAccount.objects.filter(
        account_type=AccountType.LIABILITY,
        is_active=True
    ).prefetch_related('sub_accounts')

    # Get all equity accounts
    equity_accounts = MainAccount.objects.filter(
        account_type=AccountType.EQUITY,
        is_active=True
    ).prefetch_related('sub_accounts')

    # Get revenue and expense accounts to calculate net income
    revenues = MainAccount.objects.filter(
        account_type=AccountType.REVENUE,
        is_active=True
    ).prefetch_related('sub_accounts')

    expenses = MainAccount.objects.filter(
        account_type=AccountType.EXPENSE,
        is_active=True
    ).prefetch_related('sub_accounts')

    # Calculate totals
    total_assets = sum(account.get_balance() for account in assets)
    total_liabilities = sum(account.get_balance() for account in liabilities)
    total_equity = sum(account.get_balance() for account in equity_accounts)

    # Calculate net income
    total_revenue = sum(account.get_balance() for account in revenues)
    total_expenses = sum(account.get_balance() for account in expenses)
    net_income = total_revenue - total_expenses

    context = {
        'assets': assets,
        'liabilities': liabilities,
        'equity_accounts': equity_accounts,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_equity': total_equity,
        'net_income': net_income,
        'total_equity_with_income': total_equity + net_income,
        'total_liabilities_equity': total_liabilities + total_equity + net_income,
    }

    return render(request, 'reports/balance_sheet.html', context)


@login_required
def income_statement(request):
    """
    Income Statement (Profit & Loss)
    Shows: Revenue - Expenses = Net Income
    """
    # Get all revenue accounts
    revenues = MainAccount.objects.filter(
        account_type=AccountType.REVENUE,
        is_active=True
    ).prefetch_related('sub_accounts')

    # Get all expense accounts
    expenses = MainAccount.objects.filter(
        account_type=AccountType.EXPENSE,
        is_active=True
    ).prefetch_related('sub_accounts')

    # Separate Cost of Goods Sold (5000) from other expenses
    cogs_accounts = MainAccount.objects.filter(
        account_type=AccountType.EXPENSE,
        code__startswith='5000',
        is_active=True
    ).prefetch_related('sub_accounts')

    operating_expenses = MainAccount.objects.filter(
        account_type=AccountType.EXPENSE,
        is_active=True
    ).exclude(code__startswith='5000').prefetch_related('sub_accounts')

    # Calculate totals
    total_revenue = sum(account.get_balance() for account in revenues)
    total_cogs = sum(account.get_balance() for account in cogs_accounts)
    total_operating = sum(account.get_balance() for account in operating_expenses)
    total_expenses = total_cogs + total_operating
    gross_profit = total_revenue - total_cogs
    net_income = total_revenue - total_expenses

    context = {
        'revenues': revenues,
        'cogs_accounts': cogs_accounts,
        'operating_expenses': operating_expenses,
        'expenses': expenses,
        'total_revenue': total_revenue,
        'total_cogs': total_cogs,
        'gross_profit': gross_profit,
        'total_operating': total_operating,
        'total_expenses': total_expenses,
        'net_income': net_income,
    }

    return render(request, 'reports/income_statement.html', context)


@login_required
def trial_balance(request):
    """
    Trial Balance Report
    Lists all accounts with their debit and credit balances
    """
    # Get all active accounts grouped by type
    accounts_by_type = {}

    for account_type in AccountType:
        main_accounts = MainAccount.objects.filter(
            account_type=account_type.value,
            is_active=True
        ).prefetch_related('sub_accounts')

        if main_accounts.exists():
            accounts_data = []
            for main_account in main_accounts:
                for sub_account in main_account.sub_accounts.filter(is_active=True):
                    balance = sub_account.get_balance()
                    normal_balance = sub_account.get_normal_balance()

                    if normal_balance == 'DEBIT':
                        debit = balance if balance > 0 else Decimal('0')
                        credit = abs(balance) if balance < 0 else Decimal('0')
                    else:
                        credit = balance if balance > 0 else Decimal('0')
                        debit = abs(balance) if balance < 0 else Decimal('0')

                    accounts_data.append({
                        'sub_account': sub_account,
                        'main_account': main_account,
                        'debit': debit,
                        'credit': credit,
                    })

            if accounts_data:
                accounts_by_type[account_type] = accounts_data

    # Calculate grand totals
    total_debits = Decimal('0')
    total_credits = Decimal('0')

    for accounts in accounts_by_type.values():
        for account_data in accounts:
            total_debits += account_data['debit']
            total_credits += account_data['credit']

    context = {
        'accounts_by_type': accounts_by_type,
        'total_debits': total_debits,
        'total_credits': total_credits,
        'is_balanced': abs(total_debits - total_credits) < Decimal('0.01'),
    }

    return render(request, 'reports/trial_balance.html', context)


@login_required
def cash_flow(request):
    """
    Statement of Cash Flows
    Shows cash movements from operating, investing, and financing activities
    """
    # Get all cash accounts (1000 series)
    cash_accounts = SubAccount.objects.filter(
        main_account__code__startswith='1000',
        is_active=True
    ).select_related('main_account')

    # Calculate beginning and ending cash balances
    total_cash = sum(account.get_balance() for account in cash_accounts)

    # Get all cash transactions categorized by activity type
    operating_activities = []
    investing_activities = []
    financing_activities = []

    for cash_account in cash_accounts:
        lines = cash_account.transaction_lines.filter(
            journal_entry__is_posted=True
        ).select_related('journal_entry', 'sub_account').order_by('journal_entry__date')

        for line in lines:
            # Determine cash flow direction
            if line.debit > 0:  # Cash increase
                amount = line.debit
                is_inflow = True
            else:  # Cash decrease
                amount = line.credit
                is_inflow = False

            # Get the other account(s) in this journal entry (non-cash accounts)
            other_lines = line.journal_entry.lines.exclude(
                sub_account__main_account__code__startswith='1000'
            ).select_related('sub_account')

            # Categorize by account type/code
            entry_data = {
                'date': line.journal_entry.date,
                'description': line.journal_entry.description,  # Use journal entry description
                'amount': amount,
                'is_inflow': is_inflow,
                'entry_number': line.journal_entry.entry_number,
            }

            # Operating: Revenue (4xxx), Expenses (5xxx), Current Assets (11xx), Current Liabilities (20xx)
            # Investing: Fixed Assets (13xx-19xx), Long-term Investments (16xx)
            # Financing: Long-term Liabilities (21xx-29xx), Equity (3xxx)

            # Determine category based on the other account(s) in the transaction
            categorized = False
            for other_line in other_lines:
                other_code = other_line.sub_account.code

                # Financing activities (loans, equity)
                if (other_code.startswith('21') or  # Long-term Liabilities (2100-2199)
                    other_code.startswith('22') or  # Notes Payable (2200-2299)
                    other_code.startswith('23') or  # Other long-term liabilities
                    other_code.startswith('24') or
                    other_code.startswith('25') or
                    other_code.startswith('26') or
                    other_code.startswith('27') or
                    other_code.startswith('28') or
                    other_code.startswith('29') or
                    other_code.startswith('3')):    # Equity (3000-3999)
                    financing_activities.append(entry_data)
                    categorized = True
                    break

                # Investing activities (fixed assets, long-term investments)
                elif (other_code.startswith('13') or  # Property, Plant & Equipment (1300-1399)
                      other_code.startswith('14') or  # Accumulated Depreciation (1400-1499)
                      other_code.startswith('15') or  # Land, Buildings (1500-1599)
                      other_code.startswith('16') or  # Long-term investments (1600-1699)
                      other_code.startswith('17') or  # Intangible Assets (1700-1799)
                      other_code.startswith('18') or  # Other long-term assets
                      other_code.startswith('19')):   # Other long-term assets
                    investing_activities.append(entry_data)
                    categorized = True
                    break

                # Operating activities (revenue, expenses, working capital changes)
                elif (other_code.startswith('4') or   # Revenue (4000-4999)
                      other_code.startswith('5') or   # Expenses (5000-5999)
                      other_code.startswith('11') or  # Current Assets - AR, Inventory (1100-1199)
                      other_code.startswith('12') or  # Current Assets - Prepaid, etc. (1200-1299)
                      other_code.startswith('20')):   # Current Liabilities - AP, etc. (2000-2099)
                    operating_activities.append(entry_data)
                    categorized = True
                    break

            # Default to operating if unclear
            if not categorized:
                operating_activities.append(entry_data)

    # Sort activities: inflows first (positive), then outflows (negative)
    operating_activities.sort(key=lambda x: (not x['is_inflow'], x['date']))
    investing_activities.sort(key=lambda x: (not x['is_inflow'], x['date']))
    financing_activities.sort(key=lambda x: (not x['is_inflow'], x['date']))

    # Calculate net cash flow by category
    operating_net = sum(
        (t['amount'] if t['is_inflow'] else -t['amount'])
        for t in operating_activities
    )
    investing_net = sum(
        (t['amount'] if t['is_inflow'] else -t['amount'])
        for t in investing_activities
    )
    financing_net = sum(
        (t['amount'] if t['is_inflow'] else -t['amount'])
        for t in financing_activities
    )

    net_change_in_cash = operating_net + investing_net + financing_net

    context = {
        'operating_activities': operating_activities,
        'investing_activities': investing_activities,
        'financing_activities': financing_activities,
        'operating_net': operating_net,
        'investing_net': investing_net,
        'financing_net': financing_net,
        'net_change_in_cash': net_change_in_cash,
        'ending_cash': total_cash,
        'beginning_cash': total_cash - net_change_in_cash,
    }

    return render(request, 'reports/cash_flow.html', context)
