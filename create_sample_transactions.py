#!/usr/bin/env python
"""
Script to create sample transactions for the accounting system.
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_acas.settings')
django.setup()

from transactions.models import JournalEntry, TransactionLine
from accounts.models import SubAccount
from django.contrib.auth.models import User
from decimal import Decimal

# Get the admin user for audit fields
admin_user = User.objects.get(username='admin')

# Clear existing transactions
TransactionLine.objects.all().delete()
JournalEntry.objects.all().delete()

print("Creating Sample Transactions...")
print("=" * 60)

# Helper function to get sub-accounts
def get_sub(code):
    return SubAccount.objects.get(code=code)

# ============= Transaction 1: Owner's Initial Investment =============
print("\n[Transaction 1] Owner's Initial Investment - $50,000")
je1 = JournalEntry.objects.create(
    entry_number='JE-2024-001',
    date=date(2024, 1, 1),
    description="Owner's initial capital investment in business",
    reference='INV-001',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je1,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Cash received from owner',
    debit=Decimal('50000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je1,
    sub_account=get_sub('3001'),  # Common Stock
    description="Owner's capital contribution",
    debit=Decimal('0.00'),
    credit=Decimal('50000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je1.post(user=admin_user)
print(f"  Posted: {je1.entry_number} - Balanced: ${je1.get_total_debits()}")

# ============= Transaction 2: Purchase Office Equipment =============
print("\n[Transaction 2] Purchase Office Equipment - $15,000")
je2 = JournalEntry.objects.create(
    entry_number='JE-2024-002',
    date=date(2024, 1, 5),
    description='Purchased office equipment for business operations',
    reference='PO-1001',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je2,
    sub_account=get_sub('1303'),  # Equipment
    description='Office computers and furniture',
    debit=Decimal('15000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je2,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Payment for equipment',
    debit=Decimal('0.00'),
    credit=Decimal('15000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je2.post(user=admin_user)
print(f"  Posted: {je2.entry_number} - Balanced: ${je2.get_total_debits()}")

# ============= Transaction 3: Purchase Inventory on Credit =============
print("\n[Transaction 3] Purchase Inventory on Credit - $8,500")
je3 = JournalEntry.objects.create(
    entry_number='JE-2024-003',
    date=date(2024, 1, 10),
    description='Purchased merchandise inventory on credit',
    reference='PO-1002',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je3,
    sub_account=get_sub('1203'),  # Merchandise Inventory
    description='Inventory for resale',
    debit=Decimal('8500.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je3,
    sub_account=get_sub('2001'),  # Trade Payables
    description='Amount owed to supplier',
    debit=Decimal('0.00'),
    credit=Decimal('8500.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je3.post(user=admin_user)
print(f"  Posted: {je3.entry_number} - Balanced: ${je3.get_total_debits()}")

# ============= Transaction 4: Make Sales on Credit =============
print("\n[Transaction 4] Sales on Credit - $12,000")
je4 = JournalEntry.objects.create(
    entry_number='JE-2024-004',
    date=date(2024, 1, 15),
    description='Sales to customers on credit',
    reference='INV-2001',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je4,
    sub_account=get_sub('1101'),  # Trade Receivables
    description='Amount owed by customers',
    debit=Decimal('12000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je4,
    sub_account=get_sub('4001'),  # Product Sales
    description='Sales revenue',
    debit=Decimal('0.00'),
    credit=Decimal('12000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je4.post(user=admin_user)
print(f"  Posted: {je4.entry_number} - Balanced: ${je4.get_total_debits()}")

# ============= Transaction 5: Record Cost of Goods Sold =============
print("\n[Transaction 5] Cost of Goods Sold - $5,000")
je5 = JournalEntry.objects.create(
    entry_number='JE-2024-005',
    date=date(2024, 1, 15),
    description='Cost of goods sold for sales transaction',
    reference='INV-2001-COGS',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je5,
    sub_account=get_sub('5001'),  # Purchase of Materials
    description='Cost of inventory sold',
    debit=Decimal('5000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je5,
    sub_account=get_sub('1203'),  # Merchandise Inventory
    description='Reduction in inventory',
    debit=Decimal('0.00'),
    credit=Decimal('5000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je5.post(user=admin_user)
print(f"  Posted: {je5.entry_number} - Balanced: ${je5.get_total_debits()}")

# ============= Transaction 6: Collect Cash from Customer =============
print("\n[Transaction 6] Collect Cash from Customer - $7,000")
je6 = JournalEntry.objects.create(
    entry_number='JE-2024-006',
    date=date(2024, 1, 20),
    description='Received payment from customer',
    reference='REC-3001',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je6,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Cash received',
    debit=Decimal('7000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je6,
    sub_account=get_sub('1101'),  # Trade Receivables
    description='Customer payment received',
    debit=Decimal('0.00'),
    credit=Decimal('7000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je6.post(user=admin_user)
print(f"  Posted: {je6.entry_number} - Balanced: ${je6.get_total_debits()}")

# ============= Transaction 7: Pay Supplier =============
print("\n[Transaction 7] Pay Supplier - $3,500")
je7 = JournalEntry.objects.create(
    entry_number='JE-2024-007',
    date=date(2024, 1, 25),
    description='Payment to supplier for inventory purchase',
    reference='CHK-4001',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je7,
    sub_account=get_sub('2001'),  # Trade Payables
    description='Payment to supplier',
    debit=Decimal('3500.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je7,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Cash paid',
    debit=Decimal('0.00'),
    credit=Decimal('3500.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je7.post(user=admin_user)
print(f"  Posted: {je7.entry_number} - Balanced: ${je7.get_total_debits()}")

# ============= Transaction 8: Pay Monthly Rent =============
print("\n[Transaction 8] Pay Monthly Rent - $2,000")
je8 = JournalEntry.objects.create(
    entry_number='JE-2024-008',
    date=date(2024, 2, 1),
    description='Monthly rent payment for office space',
    reference='CHK-4002',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je8,
    sub_account=get_sub('5102'),  # Rent Expense
    description='February rent',
    debit=Decimal('2000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je8,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Rent payment',
    debit=Decimal('0.00'),
    credit=Decimal('2000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je8.post(user=admin_user)
print(f"  Posted: {je8.entry_number} - Balanced: ${je8.get_total_debits()}")

# ============= Transaction 9: Pay Salaries =============
print("\n[Transaction 9] Pay Employee Salaries - $4,500")
je9 = JournalEntry.objects.create(
    entry_number='JE-2024-009',
    date=date(2024, 2, 5),
    description='Monthly salary payment to employees',
    reference='PAY-2024-02',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je9,
    sub_account=get_sub('5101'),  # Salaries & Wages
    description='Employee salaries',
    debit=Decimal('4500.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je9,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Salary payments',
    debit=Decimal('0.00'),
    credit=Decimal('4500.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je9.post(user=admin_user)
print(f"  Posted: {je9.entry_number} - Balanced: ${je9.get_total_debits()}")

# ============= Transaction 10: Receive Bank Loan =============
print("\n[Transaction 10] Receive Bank Loan - $20,000")
je10 = JournalEntry.objects.create(
    entry_number='JE-2024-010',
    date=date(2024, 2, 10),
    description='Received bank loan for business expansion',
    reference='LOAN-5001',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je10,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Loan proceeds received',
    debit=Decimal('20000.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je10,
    sub_account=get_sub('2102'),  # Long-term Loans
    description='Bank loan payable',
    debit=Decimal('0.00'),
    credit=Decimal('20000.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je10.post(user=admin_user)
print(f"  Posted: {je10.entry_number} - Balanced: ${je10.get_total_debits()}")

# ============= Transaction 11: Pay Utilities =============
print("\n[Transaction 11] Pay Utilities - $350")
je11 = JournalEntry.objects.create(
    entry_number='JE-2024-011',
    date=date(2024, 2, 15),
    description='Payment for electricity and internet',
    reference='CHK-4003',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je11,
    sub_account=get_sub('5103'),  # Utilities
    description='Monthly utilities',
    debit=Decimal('350.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je11,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Utilities payment',
    debit=Decimal('0.00'),
    credit=Decimal('350.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je11.post(user=admin_user)
print(f"  Posted: {je11.entry_number} - Balanced: ${je11.get_total_debits()}")

# ============= Transaction 12: Service Revenue (Cash) =============
print("\n[Transaction 12] Service Revenue - Cash Sale - $3,200")
je12 = JournalEntry.objects.create(
    entry_number='JE-2024-012',
    date=date(2024, 2, 20),
    description='Cash received for consulting services',
    reference='INV-2002',
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je12,
    sub_account=get_sub('1003'),  # Cash in Bank - Checking
    description='Cash received',
    debit=Decimal('3200.00'),
    credit=Decimal('0.00'),
    created_by=admin_user,
    updated_by=admin_user
)

TransactionLine.objects.create(
    journal_entry=je12,
    sub_account=get_sub('4002'),  # Service Revenue
    description='Consulting service revenue',
    debit=Decimal('0.00'),
    credit=Decimal('3200.00'),
    created_by=admin_user,
    updated_by=admin_user
)

je12.post(user=admin_user)
print(f"  Posted: {je12.entry_number} - Balanced: ${je12.get_total_debits()}")

# ============= SUMMARY =============
print("\n" + "=" * 60)
print("SAMPLE TRANSACTIONS CREATED SUCCESSFULLY!")
print("=" * 60)
print(f"Total Journal Entries: {JournalEntry.objects.count()}")
print(f"Total Transaction Lines: {TransactionLine.objects.count()}")
print(f"Posted Entries: {JournalEntry.objects.filter(is_posted=True).count()}")
print("\nSummary of Account Balances:")
print("-" * 60)

# Show some key balances
print(f"Cash in Bank - Checking: ${get_sub('1003').get_balance():,.2f}")
print(f"Trade Receivables: ${get_sub('1101').get_balance():,.2f}")
print(f"Merchandise Inventory: ${get_sub('1203').get_balance():,.2f}")
print(f"Equipment: ${get_sub('1303').get_balance():,.2f}")
print(f"Trade Payables: ${get_sub('2001').get_balance():,.2f}")
print(f"Long-term Loans: ${get_sub('2102').get_balance():,.2f}")
print(f"Common Stock (Owner Capital): ${get_sub('3001').get_balance():,.2f}")
print(f"Product Sales: ${get_sub('4001').get_balance():,.2f}")
print(f"Service Revenue: ${get_sub('4002').get_balance():,.2f}")
print(f"Cost of Goods Sold: ${get_sub('5001').get_balance():,.2f}")
print(f"Salaries & Wages: ${get_sub('5101').get_balance():,.2f}")
print(f"Rent Expense: ${get_sub('5102').get_balance():,.2f}")

print("\n" + "=" * 60)
print("You can now view these transactions in Django Admin!")
print("Go to http://127.0.0.1:8000/admin/")
