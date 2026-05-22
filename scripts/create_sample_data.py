#!/usr/bin/env python
"""
Script to populate the Chart of Accounts with sample data.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_acas.settings')
django.setup()

from accounts.models import MainAccount, SubAccount, AccountType
from django.contrib.auth.models import User

# Get the admin user for audit fields
admin_user = User.objects.get(username='admin')

# Clear existing data (if any)
SubAccount.objects.all().delete()
MainAccount.objects.all().delete()

print("Creating Main Accounts and Sub Accounts...")
print("=" * 60)

# ============= ASSETS =============
print("\n[ASSET ACCOUNTS]")

# 1. Cash
cash = MainAccount.objects.create(
    code='1000',
    name='Cash',
    account_type=AccountType.ASSET,
    description='All cash accounts',
    created_by=admin_user,
    updated_by=admin_user
)
print(f"[OK] Created: {cash}")

SubAccount.objects.create(
    main_account=cash, code='1001', name='Cash on Hand',
    description='Physical cash in office', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=cash, code='1002', name='Petty Cash',
    description='Small cash fund for minor expenses', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=cash, code='1003', name='Cash in Bank - Checking',
    description='Main business checking account', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=cash, code='1004', name='Cash in Bank - Savings',
    description='Business savings account', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 4 sub-accounts under Cash")

# 2. Accounts Receivable
ar = MainAccount.objects.create(
    code='1100', name='Accounts Receivable', account_type=AccountType.ASSET,
    description='Money owed by customers', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {ar}")

SubAccount.objects.create(
    main_account=ar, code='1101', name='Trade Receivables',
    description='Receivables from regular customers', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=ar, code='1102', name='Other Receivables',
    description='Non-trade receivables', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 2 sub-accounts under Accounts Receivable")

# 3. Inventory
inventory = MainAccount.objects.create(
    code='1200', name='Inventory', account_type=AccountType.ASSET,
    description='Goods held for sale', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {inventory}")

SubAccount.objects.create(
    main_account=inventory, code='1201', name='Raw Materials',
    description='Materials for production', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=inventory, code='1202', name='Finished Goods',
    description='Completed products ready for sale', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=inventory, code='1203', name='Merchandise Inventory',
    description='Goods purchased for resale', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 3 sub-accounts under Inventory")

# 4. Fixed Assets
fixed_assets = MainAccount.objects.create(
    code='1300', name='Fixed Assets', account_type=AccountType.ASSET,
    description='Long-term tangible assets', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {fixed_assets}")

SubAccount.objects.create(
    main_account=fixed_assets, code='1301', name='Land',
    description='Real estate owned', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=fixed_assets, code='1302', name='Buildings',
    description='Office and warehouse buildings', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=fixed_assets, code='1303', name='Equipment',
    description='Machinery and equipment', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=fixed_assets, code='1304', name='Vehicles',
    description='Company vehicles', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=fixed_assets, code='1305', name='Furniture & Fixtures',
    description='Office furniture', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 5 sub-accounts under Fixed Assets")

# ============= LIABILITIES =============
print("\n[LIABILITY ACCOUNTS]")

# 5. Accounts Payable
ap = MainAccount.objects.create(
    code='2000', name='Accounts Payable', account_type=AccountType.LIABILITY,
    description='Money owed to suppliers', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {ap}")

SubAccount.objects.create(
    main_account=ap, code='2001', name='Trade Payables',
    description='Payables to regular suppliers', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=ap, code='2002', name='Other Payables',
    description='Non-trade payables', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 2 sub-accounts under Accounts Payable")

# 6. Loans Payable
loans = MainAccount.objects.create(
    code='2100', name='Loans Payable', account_type=AccountType.LIABILITY,
    description='Bank loans and notes payable', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {loans}")

SubAccount.objects.create(
    main_account=loans, code='2101', name='Short-term Loans',
    description='Loans due within one year', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=loans, code='2102', name='Long-term Loans',
    description='Loans due after one year', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=loans, code='2103', name='Mortgage Payable',
    description='Real estate mortgages', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 3 sub-accounts under Loans Payable")

# 7. Accrued Expenses
accrued = MainAccount.objects.create(
    code='2200', name='Accrued Expenses', account_type=AccountType.LIABILITY,
    description='Expenses incurred but not yet paid', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {accrued}")

SubAccount.objects.create(
    main_account=accrued, code='2201', name='Salaries Payable',
    description='Unpaid employee salaries', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=accrued, code='2202', name='Interest Payable',
    description='Accrued interest on loans', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=accrued, code='2203', name='Taxes Payable',
    description='Unpaid taxes', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 3 sub-accounts under Accrued Expenses")

# ============= EQUITY =============
print("\n[EQUITY ACCOUNTS]")

# 8. Owner's Capital
capital = MainAccount.objects.create(
    code='3000', name="Owner's Capital", account_type=AccountType.EQUITY,
    description='Owner investment in business', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {capital}")

SubAccount.objects.create(
    main_account=capital, code='3001', name='Common Stock',
    description='Shares issued to owners', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=capital, code='3002', name='Additional Paid-in Capital',
    description='Capital contributed above par value', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 2 sub-accounts under Owner's Capital")

# 9. Retained Earnings
retained = MainAccount.objects.create(
    code='3100', name='Retained Earnings', account_type=AccountType.EQUITY,
    description='Accumulated profits', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {retained}")

SubAccount.objects.create(
    main_account=retained, code='3101', name='Current Year Earnings',
    description='Profit for current fiscal year', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=retained, code='3102', name='Prior Year Earnings',
    description='Accumulated earnings from prior years', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 2 sub-accounts under Retained Earnings")

# 10. Owner's Drawings
drawings = MainAccount.objects.create(
    code='3200', name="Owner's Drawings", account_type=AccountType.EQUITY,
    description='Owner withdrawals from business', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {drawings}")

SubAccount.objects.create(
    main_account=drawings, code='3201', name='Cash Withdrawals',
    description='Cash taken by owner', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=drawings, code='3202', name='Dividends',
    description='Dividends paid to shareholders', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 2 sub-accounts under Owner's Drawings")

# ============= REVENUE =============
print("\n[REVENUE ACCOUNTS]")

# 11. Sales Revenue
sales = MainAccount.objects.create(
    code='4000', name='Sales Revenue', account_type=AccountType.REVENUE,
    description='Income from primary business operations', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {sales}")

SubAccount.objects.create(
    main_account=sales, code='4001', name='Product Sales',
    description='Revenue from selling products', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=sales, code='4002', name='Service Revenue',
    description='Revenue from services provided', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=sales, code='4003', name='Consulting Revenue',
    description='Revenue from consulting services', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 3 sub-accounts under Sales Revenue")

# 12. Other Income
other_income = MainAccount.objects.create(
    code='4100', name='Other Income', account_type=AccountType.REVENUE,
    description='Non-operating income', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {other_income}")

SubAccount.objects.create(
    main_account=other_income, code='4101', name='Interest Income',
    description='Interest earned on deposits', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=other_income, code='4102', name='Rental Income',
    description='Income from property rentals', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=other_income, code='4103', name='Gain on Sale of Assets',
    description='Profit from selling assets', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 3 sub-accounts under Other Income")

# ============= EXPENSES =============
print("\n[EXPENSE ACCOUNTS]")

# 13. Cost of Goods Sold
cogs = MainAccount.objects.create(
    code='5000', name='Cost of Goods Sold', account_type=AccountType.EXPENSE,
    description='Direct costs of products sold', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {cogs}")

SubAccount.objects.create(
    main_account=cogs, code='5001', name='Purchase of Materials',
    description='Raw materials purchased', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=cogs, code='5002', name='Direct Labor',
    description='Labor directly tied to production', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=cogs, code='5003', name='Manufacturing Overhead',
    description='Indirect production costs', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 3 sub-accounts under Cost of Goods Sold")

# 14. Operating Expenses
operating = MainAccount.objects.create(
    code='5100', name='Operating Expenses', account_type=AccountType.EXPENSE,
    description='General business operating costs', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {operating}")

SubAccount.objects.create(
    main_account=operating, code='5101', name='Salaries & Wages',
    description='Employee compensation', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=operating, code='5102', name='Rent Expense',
    description='Office and facility rent', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=operating, code='5103', name='Utilities',
    description='Electricity, water, internet', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=operating, code='5104', name='Office Supplies',
    description='General office supplies', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=operating, code='5105', name='Insurance',
    description='Business insurance premiums', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=operating, code='5106', name='Advertising & Marketing',
    description='Marketing and promotional costs', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 6 sub-accounts under Operating Expenses")

# 15. Administrative Expenses
admin_exp = MainAccount.objects.create(
    code='5200', name='Administrative Expenses', account_type=AccountType.EXPENSE,
    description='Administrative and general expenses', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {admin_exp}")

SubAccount.objects.create(
    main_account=admin_exp, code='5201', name='Professional Fees',
    description='Legal and accounting fees', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=admin_exp, code='5202', name='Bank Charges',
    description='Banking fees and charges', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=admin_exp, code='5203', name='Depreciation',
    description='Asset depreciation expense', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=admin_exp, code='5204', name='Travel & Entertainment',
    description='Business travel costs', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 4 sub-accounts under Administrative Expenses")

# 16. Interest Expense
interest_exp = MainAccount.objects.create(
    code='5300', name='Interest Expense', account_type=AccountType.EXPENSE,
    description='Interest paid on loans', created_by=admin_user, updated_by=admin_user
)
print(f"[OK] Created: {interest_exp}")

SubAccount.objects.create(
    main_account=interest_exp, code='5301', name='Interest on Bank Loans',
    description='Interest on business loans', created_by=admin_user, updated_by=admin_user
)
SubAccount.objects.create(
    main_account=interest_exp, code='5302', name='Interest on Mortgage',
    description='Mortgage interest payments', created_by=admin_user, updated_by=admin_user
)
print(f"  Added 2 sub-accounts under Interest Expense")

# ============= SUMMARY =============
print("\n" + "=" * 60)
print("CHART OF ACCOUNTS CREATED SUCCESSFULLY!")
print("=" * 60)
print(f"Total Main Accounts: {MainAccount.objects.count()}")
print(f"Total Sub Accounts: {SubAccount.objects.count()}")
print("\nBreakdown by Account Type:")
print(f"  Assets:      {MainAccount.objects.filter(account_type=AccountType.ASSET).count()} main accounts, {SubAccount.objects.filter(main_account__account_type=AccountType.ASSET).count()} sub-accounts")
print(f"  Liabilities: {MainAccount.objects.filter(account_type=AccountType.LIABILITY).count()} main accounts, {SubAccount.objects.filter(main_account__account_type=AccountType.LIABILITY).count()} sub-accounts")
print(f"  Equity:      {MainAccount.objects.filter(account_type=AccountType.EQUITY).count()} main accounts, {SubAccount.objects.filter(main_account__account_type=AccountType.EQUITY).count()} sub-accounts")
print(f"  Revenue:     {MainAccount.objects.filter(account_type=AccountType.REVENUE).count()} main accounts, {SubAccount.objects.filter(main_account__account_type=AccountType.REVENUE).count()} sub-accounts")
print(f"  Expenses:    {MainAccount.objects.filter(account_type=AccountType.EXPENSE).count()} main accounts, {SubAccount.objects.filter(main_account__account_type=AccountType.EXPENSE).count()} sub-accounts")
print("\nYou can now view these in Django Admin!")
