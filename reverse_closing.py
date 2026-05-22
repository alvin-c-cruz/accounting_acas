#!/usr/bin/env python
"""
Reverse/delete the closing entry to restore revenue and expense account balances
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_acas.settings')
django.setup()

from transactions.models import JournalEntry
from accounts.models import SubAccount

# Find the closing entry
closing_entry = JournalEntry.objects.filter(reference='CLOSING').first()

if not closing_entry:
    print("No closing entry found.")
    exit(0)

print(f"Found closing entry: {closing_entry.entry_number}")
print(f"Date: {closing_entry.date}")
print(f"Description: {closing_entry.description}")
print(f"Posted: {closing_entry.is_posted}")
print()

# Show what will be deleted
print("Lines in this entry:")
for line in closing_entry.lines.all():
    print(f"  {line.sub_account.code} - {line.sub_account.name}")
    print(f"    Debit: ${line.debit}, Credit: ${line.credit}")

print()

# Check Current Year Earnings before deletion
cye = SubAccount.objects.filter(code='3101').first()
if cye:
    print(f"Current Year Earnings balance BEFORE deletion: ${cye.get_balance()}")

# Delete the entry
closing_entry.delete()
print()
print(f"Closing entry {closing_entry.entry_number} has been deleted.")

# Check balances after deletion
if cye:
    print(f"Current Year Earnings balance AFTER deletion: ${cye.get_balance()}")

print()
print("Revenue and expense accounts have been restored to their pre-closing balances.")
