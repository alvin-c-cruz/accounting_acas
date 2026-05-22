#!/usr/bin/env python
"""
Create closing entries to transfer net income to Current Year Earnings
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_acas.settings')
django.setup()

from django.contrib.auth.models import User
from transactions.models import JournalEntry, TransactionLine
from accounts.models import MainAccount, SubAccount, AccountType
from django.db import transaction
from datetime import date

# Get the admin user
user = User.objects.first()
if not user:
    print("Error: No user found. Please create a user first.")
    exit(1)

# Get Current Year Earnings account
current_year_earnings = SubAccount.objects.filter(code='3101').first()
if not current_year_earnings:
    print("Error: Current Year Earnings account (3101) not found.")
    exit(1)

# Calculate net income from revenue and expense accounts
revenues = MainAccount.objects.filter(account_type=AccountType.REVENUE, is_active=True)
expenses = MainAccount.objects.filter(account_type=AccountType.EXPENSE, is_active=True)

total_revenue = sum(account.get_balance() for account in revenues)
total_expenses = sum(account.get_balance() for account in expenses)
net_income = total_revenue - total_expenses

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Expenses: ${total_expenses:,.2f}")
print(f"Net Income: ${net_income:,.2f}")
print()

if net_income == 0:
    print("Net income is $0.00. No closing entry needed.")
    exit(0)

# Get the next entry number
last_entry = JournalEntry.objects.order_by('-entry_number').first()
if last_entry:
    try:
        next_number = str(int(last_entry.entry_number) + 1).zfill(4)
    except:
        next_number = 'CE001'
else:
    next_number = 'CE001'

print(f"Creating closing entry {next_number}...")
print()

# Create the closing entry
with transaction.atomic():
    # Create journal entry
    entry = JournalEntry.objects.create(
        entry_number=next_number,
        date=date.today(),
        description="Period closing entry - Transfer net income to Current Year Earnings",
        reference="CLOSING",
        created_by=user,
        updated_by=user,
        is_posted=False
    )

    # Close revenue accounts (debit revenue accounts to zero them out)
    for main_account in revenues:
        for sub_account in main_account.sub_accounts.filter(is_active=True):
            balance = sub_account.get_balance()
            if balance > 0:
                TransactionLine.objects.create(
                    journal_entry=entry,
                    sub_account=sub_account,
                    description=f"Close {sub_account.name} to Current Year Earnings",
                    debit=balance,
                    credit=Decimal('0'),
                    created_by=user,
                    updated_by=user
                )
                print(f"  Debit {sub_account.code} - {sub_account.name}: ${balance:,.2f}")

    # Close expense accounts (credit expense accounts to zero them out)
    for main_account in expenses:
        for sub_account in main_account.sub_accounts.filter(is_active=True):
            balance = sub_account.get_balance()
            if balance > 0:
                TransactionLine.objects.create(
                    journal_entry=entry,
                    sub_account=sub_account,
                    description=f"Close {sub_account.name} to Current Year Earnings",
                    debit=Decimal('0'),
                    credit=balance,
                    created_by=user,
                    updated_by=user
                )
                print(f"  Credit {sub_account.code} - {sub_account.name}: ${balance:,.2f}")

    # Credit Current Year Earnings with net income (if positive) or debit if negative
    if net_income > 0:
        TransactionLine.objects.create(
            journal_entry=entry,
            sub_account=current_year_earnings,
            description="Net income for the period",
            debit=Decimal('0'),
            credit=net_income,
            created_by=user,
            updated_by=user
        )
        print(f"  Credit {current_year_earnings.code} - {current_year_earnings.name}: ${net_income:,.2f}")
    else:
        TransactionLine.objects.create(
            journal_entry=entry,
            sub_account=current_year_earnings,
            description="Net loss for the period",
            debit=abs(net_income),
            credit=Decimal('0'),
            created_by=user,
            updated_by=user
        )
        print(f"  Debit {current_year_earnings.code} - {current_year_earnings.name}: ${abs(net_income):,.2f}")

    print()

    # Check if balanced
    if entry.is_balanced():
        print(f"[OK] Closing entry {next_number} is balanced")
        print(f"  Total debits: ${entry.get_total_debits():,.2f}")
        print(f"  Total credits: ${entry.get_total_credits():,.2f}")

        # Post the entry
        entry.post(user=user)
        print(f"[OK] Closing entry {next_number} has been posted")
    else:
        print(f"[ERROR] Closing entry is not balanced!")
        print(f"  Total debits: ${entry.get_total_debits():,.2f}")
        print(f"  Total credits: ${entry.get_total_credits():,.2f}")
        raise Exception("Closing entry is not balanced")

print()
print("Period closing complete!")
print(f"Current Year Earnings balance: ${current_year_earnings.get_balance():,.2f}")
