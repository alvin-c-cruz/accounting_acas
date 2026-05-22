#!/usr/bin/env python
"""
Quick diagnostic script to check the balance sheet state
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_acas.settings')
django.setup()

from transactions.models import JournalEntry
from accounts.models import MainAccount, AccountType
from decimal import Decimal

# Check transaction status
posted_count = JournalEntry.objects.filter(is_posted=True).count()
draft_count = JournalEntry.objects.filter(is_posted=False).count()

print(f"Posted journal entries: {posted_count}")
print(f"Draft journal entries: {draft_count}")
print()

# Calculate total debits and credits from posted transactions
total_debits = Decimal('0')
total_credits = Decimal('0')

for entry in JournalEntry.objects.filter(is_posted=True).prefetch_related('lines'):
    for line in entry.lines.all():
        total_debits += line.debit
        total_credits += line.credit

print(f"Total debits in posted transactions: ${total_debits:,.2f}")
print(f"Total credits in posted transactions: ${total_credits:,.2f}")
print(f"Difference (should be $0.00): ${total_debits - total_credits:,.2f}")
print()

# Calculate balances by account type
assets = MainAccount.objects.filter(account_type=AccountType.ASSET, is_active=True)
liabilities = MainAccount.objects.filter(account_type=AccountType.LIABILITY, is_active=True)
equity = MainAccount.objects.filter(account_type=AccountType.EQUITY, is_active=True)
revenue = MainAccount.objects.filter(account_type=AccountType.REVENUE, is_active=True)
expenses = MainAccount.objects.filter(account_type=AccountType.EXPENSE, is_active=True)

total_assets = sum(account.get_balance() for account in assets)
total_liabilities = sum(account.get_balance() for account in liabilities)
total_equity = sum(account.get_balance() for account in equity)
total_revenue = sum(account.get_balance() for account in revenue)
total_expenses = sum(account.get_balance() for account in expenses)

print("=== Account Balances ===")
print(f"Assets: ${total_assets:,.2f}")
print(f"Liabilities: ${total_liabilities:,.2f}")
print(f"Equity: ${total_equity:,.2f}")
print(f"Revenue: ${total_revenue:,.2f}")
print(f"Expenses: ${total_expenses:,.2f}")
print()

# Calculate net income
net_income = total_revenue - total_expenses
print(f"Net Income (Revenue - Expenses): ${net_income:,.2f}")
print()

# Check balance sheet equation
liabilities_plus_equity = total_liabilities + total_equity
difference = total_assets - liabilities_plus_equity

print("=== Balance Sheet Equation ===")
print(f"Assets: ${total_assets:,.2f}")
print(f"Liabilities + Equity: ${liabilities_plus_equity:,.2f}")
print(f"Difference: ${difference:,.2f}")
print()

if abs(difference) < 0.01:
    print("✓ Balance Sheet is BALANCED")
else:
    print("⚠ Balance Sheet is NOT BALANCED")
    print()
    print("Possible reasons:")
    print("1. Net income hasn't been closed to equity (Retained Earnings)")
    print("2. There are unposted transactions")
    print("3. Revenue/Expense accounts have balances that need to be closed")
    print()
    print(f"If net income (${net_income:,.2f}) is added to equity:")
    print(f"  Assets: ${total_assets:,.2f}")
    print(f"  Liabilities + Equity + Net Income: ${liabilities_plus_equity + net_income:,.2f}")
    print(f"  New Difference: ${total_assets - (liabilities_plus_equity + net_income):,.2f}")
