# Utility Scripts

This directory contains utility scripts for managing the accounting system.

## Production Utilities

### check_balance.py
**Purpose**: Diagnostic script to verify ledger integrity and balance sheet equation.

**Usage**:
```bash
python scripts/check_balance.py
```

**What it checks**:
- Posted vs draft transaction counts
- Total debits vs total credits (must equal)
- Balance by account type
- Balance sheet equation: Assets = Liabilities + Equity
- Net income calculation
- Color-coded terminal output with status indicators

**When to use**:
- After posting multiple transactions
- Before period closing
- When balance sheet doesn't balance
- Regular data integrity checks

---

### close_period.py
**Purpose**: Create closing entries to transfer net income to retained earnings.

**Usage**:
```bash
python scripts/close_period.py
```

**What it does**:
1. Debits all revenue accounts (zeros them out)
2. Credits all expense accounts (zeros them out)
3. Transfers net income to "Current Year Earnings" (account 3101)
4. Validates the closing entry is balanced
5. Posts the closing entry automatically

**Requirements**:
- Sub-account 3101 "Current Year Earnings" must exist
- Should be run at end of accounting period (monthly, quarterly, yearly)

**Important**: This creates permanent journal entries. Use `reverse_closing.py` if you need to undo.

---

### reverse_closing.py
**Purpose**: Reverse/delete previously created closing entries.

**Usage**:
```bash
python scripts/reverse_closing.py
```

**What it does**:
- Finds the most recent closing entry
- Deletes it to restore revenue and expense account balances
- Useful for corrections or if closing was done prematurely

**When to use**:
- Closing entry was created by mistake
- Need to add more transactions to the closed period
- Corrections needed before final period close

---

## Development & Testing Utilities

### create_sample_data.py
**Purpose**: Populate the chart of accounts with sample data.

**Usage**:
```bash
python scripts/create_sample_data.py
```

**What it creates**:
- Sample main accounts (Assets, Liabilities, Equity, Revenue, Expenses)
- Sample sub-accounts with realistic names
- Account classes for expense categorization (COGS, Selling, Administrative)
- Properly linked 3-level hierarchy

**When to use**:
- Fresh database setup for development
- Demo purposes
- Testing the application
- Learning the account structure

---

### create_sample_transactions.py
**Purpose**: Create sample transactions for testing and demonstration.

**Usage**:
```bash
python scripts/create_sample_transactions.py
```

**What it creates**:
- Sample journal entries with realistic descriptions
- Mix of posted and draft transactions
- Balanced debits and credits
- Various transaction types (revenue, expenses, asset purchases, etc.)

**When to use**:
- After running `create_sample_data.py`
- Testing financial reports
- Demonstrating the application
- Development and testing

---

## Running Scripts

All scripts should be run from the project root directory:

```bash
# From accounting_acas/ directory
python scripts/check_balance.py
python scripts/close_period.py
python scripts/reverse_closing.py
python scripts/create_sample_data.py
python scripts/create_sample_transactions.py
```

## Notes

- All scripts require Django to be installed and configured
- Production utilities (`check_balance`, `close_period`, `reverse_closing`) operate on real data
- Development utilities create sample data for testing only
- Always backup your database before running closing or reversal scripts
- Scripts inherit user context from Django's authentication system
