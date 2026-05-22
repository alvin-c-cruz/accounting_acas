# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Alvin Cruz Accounting Services (ACAS)** - A comprehensive online accounting system for managing financial transactions, accounts, and reports. The system provides a web-based interface for accounting operations with a focus on data integrity, accuracy, and professional double-entry bookkeeping.

### Key Features
- ✅ **3-Level Account Hierarchy** for detailed expense categorization
- ✅ **Double-Entry Bookkeeping** with automatic balance validation
- ✅ **Posting/Unposting Mechanism** for transaction lifecycle management
- ✅ **Comprehensive Financial Reports** (Balance Sheet, Income Statement, Trial Balance, Cash Flow)
- ✅ **Full Audit Trail** for all transactions and changes
- ✅ **Responsive Design** optimized for desktop, tablet, and mobile devices
- ✅ **Superuser Access Control** for administrative functions

## Critical Architecture Considerations

### Data Consistency Requirements
- Accounting data requires ACID properties (Atomicity, Consistency, Isolation, Durability)
- Implement proper transaction handling for concurrent modifications using `transaction.atomic()`
- Maintain comprehensive audit trails for all financial transactions (created_by, updated_by, timestamps)
- Handle currency precision correctly (ALWAYS use DecimalField, NEVER float)
- Protect posted transactions from modification (immutability after posting)

### Key Technical Decisions
1. **Database**: PostgreSQL for production, SQLite for development
2. **Authentication**: Django's built-in authentication system with custom login/logout views
3. **Frontend**: Django Templates (server-side rendering) with custom responsive CSS
4. **Admin Interface**: Enhanced Django Admin with custom inlines and validation
5. **Design System**: Custom "ACAS" color palette with teal primary color (#1a6473)

## Technology Stack

- **Language**: Python 3.11+
- **Web Framework**: Django 6.0.5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates with custom CSS (no framework dependencies)
- **Admin**: Django Admin (enhanced with custom forms and validation)
- **Forms**: Django Forms with formsets for transaction lines
- **Decimal Handling**: Django's `DecimalField(max_digits=19, decimal_places=2)` for all currency values
- **Version Control**: Git (assumed)

## Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Load initial data (chart of accounts, etc.)
python manage.py loaddata initial_data.json
```

## Common Commands

```bash
# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run tests
python manage.py test

# Run specific test
python manage.py test accounts.tests.test_models

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Create new app
python manage.py startapp <app_name>

# Make migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Check for issues
python manage.py check

# Lint code
ruff check .

# Format code
ruff format .
```

## Project Structure

```
accounting_acas/
├── accounting_acas/         # Project configuration
│   ├── __init__.py
│   ├── settings.py         # Django settings with custom context processors
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI config for deployment
│   └── asgi.py             # ASGI config
├── accounts/                # Chart of Accounts management
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── 0002_accountclass_subaccount_account_class.py  # 3-level hierarchy
│   ├── models.py           # MainAccount, SubAccount, AccountClass, AccountType
│   ├── views.py            # chart_of_accounts (with 3-level rendering), account_detail
│   ├── urls.py
│   ├── admin.py            # Enhanced admin with inlines and custom displays
│   ├── templates/accounts/
│   │   ├── chart_of_accounts.html    # Trial balance format with responsive design
│   │   └── account_detail.html
│   └── tests.py
├── transactions/            # Journal entries & double-entry bookkeeping
│   ├── migrations/
│   ├── models.py           # JournalEntry, TransactionLine with posting mechanism
│   ├── views.py            # CRUD operations with atomic transactions
│   ├── forms.py            # JournalEntryForm, TransactionLineFormSet
│   ├── urls.py
│   ├── admin.py            # Inline transaction lines with validation
│   ├── templates/transactions/
│   │   ├── transaction_list.html
│   │   ├── transaction_form.html     # Multi-line entry with formsets
│   │   └── transaction_detail.html
│   └── tests.py
├── reports/                 # Financial reporting
│   ├── views.py            # balance_sheet, income_statement, trial_balance, cash_flow
│   ├── urls.py
│   ├── templates/reports/
│   │   ├── index.html
│   │   ├── balance_sheet.html
│   │   ├── income_statement.html
│   │   ├── trial_balance.html
│   │   └── cash_flow.html
│   └── tests.py
├── dashboard/               # Main landing page
│   ├── views.py            # Summary statistics (assets, liabilities, equity, revenue)
│   ├── urls.py
│   ├── templates/dashboard/
│   │   └── index.html
│   └── tests.py
├── settings_app/            # Site configuration & custom auth
│   ├── models.py           # SiteSettings (singleton pattern)
│   ├── views.py            # settings_view, login_view, logout_view
│   ├── context_processors.py  # site_settings (global template access)
│   ├── admin.py
│   ├── urls.py
│   ├── templates/settings_app/
│   │   ├── login.html
│   │   └── settings.html
│   └── tests.py
├── templates/               # Shared templates
│   ├── base.html           # Main base template with navbar, footer
│   ├── base_report.html    # Report-specific base
│   └── navbar.html         # Responsive navigation with hamburger menu
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Responsive design (desktop/tablet/mobile)
│   └── js/
│       └── dashboard.js
├── staticfiles/             # Collected static files (production)
├── media/                   # User uploaded files
├── manage.py                # Django management script
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── check_balance.py         # Diagnostic: verify ledger balance
├── close_period.py          # Utility: create closing entries
├── create_sample_data.py    # Utility: generate demo data
├── reverse_closing.py       # Utility: reverse closing entries
├── .env.example
├── CLAUDE.md               # This file
└── db.sqlite3              # SQLite database (development)
```

## Django Apps Structure

The project is organized into **5 Django apps** by functional domain:

### **accounts/** - Chart of Accounts Management
- **Purpose**: Manage 3-level account hierarchy with trial balance view
- **Models**:
  - `AccountType` (Enum: ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE)
  - `MainAccount` (Top level: "Cash", "Accounts Payable")
  - `AccountClass` (Middle level: "COGS", "Selling Expenses", "Administrative")
  - `SubAccount` (Detail level: "Cash on Hand", "Office Supplies")
- **Views**:
  - `chart_of_accounts`: Trial balance with 3-level hierarchy for expenses
  - `account_detail`: Transaction history for specific account
- **Key Features**: Balance calculations, normal balance convention, responsive table design

### **transactions/** - Journal Entries & Double-Entry
- **Purpose**: Record financial transactions with double-entry validation
- **Models**:
  - `JournalEntry` (Header: date, description, reference, posting status)
  - `TransactionLine` (Detail: sub_account, debit, credit)
- **Views**: List, create, edit, detail, post, unpost
- **Key Features**:
  - Formset-based multi-line entry (4 blank lines, min 2 required)
  - Atomic transactions with `transaction.atomic()`
  - Posted entry protection (immutable after posting)
  - Balance validation (debits = credits)

### **reports/** - Financial Reporting
- **Purpose**: Generate standard accounting reports
- **Reports**:
  - Balance Sheet (Assets = Liabilities + Equity)
  - Income Statement (Revenue - Expenses with COGS breakdown)
  - Trial Balance (All accounts with debit/credit columns)
  - Cash Flow Statement (Operating/Investing/Financing activities)
- **Key Features**: Real-time calculations from posted transactions

### **dashboard/** - Main Dashboard
- **Purpose**: Financial overview and quick actions
- **Displays**: Total assets, liabilities, equity, monthly revenue
- **Quick Actions**: Links to create transactions, view accounts, generate reports

### **settings_app/** - Site Configuration & Authentication
- **Purpose**: Manage site-wide settings and custom auth
- **Models**: `SiteSettings` (company_name, copyright_text)
- **Views**: Settings management (superuser only), custom login/logout
- **Context Processor**: Makes `site_settings` available in all templates
- **Access Control**: Superuser-only settings, staff restrictions

## Testing Strategy

- Use Django's built-in `TestCase` for database tests
- Use `SimpleTestCase` for tests without database
- Test models, views, forms, and business logic
- Test double-entry bookkeeping validation
- Use `freezegun` for time-dependent tests (accounting periods)
- Test admin interface customizations

## Important Implementation Notes

### Currency and Decimal Handling
```python
from django.db import models

class Transaction(models.Model):
    # Always use DecimalField for currency
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    # Never use FloatField for currency:
    # amount = models.FloatField()  # WRONG - causes precision errors
```

### Double-Entry Bookkeeping
Every journal entry must have balanced debits and credits:
```python
class JournalEntry(models.Model):
    def clean(self):
        total_debits = sum(line.debit for line in self.lines.all())
        total_credits = sum(line.credit for line in self.lines.all())

        if total_debits != total_credits:
            raise ValidationError("Debits must equal credits")
```

### Django Admin Customization
Register all models in admin.py for easy data management:
```python
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'balance']
    list_filter = ['account_type']
    search_fields = ['code', 'name']
```

### Audit Trail
Include audit fields in all models:
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')

    class Meta:
        abstract = True
```

## 3-Level Account Hierarchy

The system implements a flexible account hierarchy that supports both 2-level and 3-level structures:

### Account Structure

```
AccountType (ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE)
    ↓
MainAccount (e.g., "5000 - Operating Expenses")
    ↓
AccountClass (Optional - for Expense accounts)
    ├── COGS - Cost of Goods Sold
    ├── SELL - Selling Expenses
    ├── ADMIN - Administrative Expenses
    └── INT - Interest Expense
    ↓
SubAccount (Detailed accounts for transaction posting)
    ├── 5001 - Raw Materials
    ├── 5002 - Direct Labor
    ├── 5100 - Advertising
    └── 5200 - Office Supplies
```

### When to Use 3-Level Hierarchy

**Use 3 levels for EXPENSE accounts** when you need categorical grouping:
- **Cost of Goods Sold** (COGS): Direct costs of producing goods/services
- **Selling Expenses** (SELL): Marketing, sales commissions, advertising
- **Administrative Expenses** (ADMIN): Office supplies, utilities, salaries
- **Interest Expense** (INT): Loan interest, financing costs

**Use 2 levels for other account types** (Asset, Liability, Equity, Revenue):
- MainAccount → SubAccount (no AccountClass needed)

### Implementation Example

```python
# Create Account Class for Expense categorization
cogs_class = AccountClass.objects.create(
    code='COGS',
    name='Cost of Goods Sold',
    main_account=expense_main_account,
    created_by=user,
    updated_by=user
)

# Create Sub-Account under Account Class
raw_materials = SubAccount.objects.create(
    code='5001',
    name='Raw Materials',
    main_account=expense_main_account,
    account_class=cogs_class,  # Links to AccountClass
    created_by=user,
    updated_by=user
)
```

### Chart of Accounts Display

The `chart_of_accounts` view automatically renders:
- **For EXPENSE accounts**: Main Account → Account Class headers → Sub-Accounts (indented)
- **For other types**: Main Account → Sub-Accounts (flat structure)

## Posting Mechanism

### Transaction Lifecycle

```
Draft → Post → [Locked] → Unpost (if corrections needed) → Post again
```

**Draft State** (`is_posted=False`):
- Editable
- Not included in financial reports
- Can be deleted
- Validation: must be balanced

**Posted State** (`is_posted=True`):
- Locked (cannot edit or delete)
- Included in all financial reports
- Timestamp recorded (`posted_at`)
- Can be unposted for corrections

### Posting Rules

```python
# Post a journal entry
entry.post(user)  # Sets is_posted=True, records updated_by and timestamp

# Unpost for corrections
entry.unpost(user)  # Sets is_posted=False, allows editing

# Protection in views
if entry.is_posted:
    messages.error(request, 'Cannot edit posted entry')
    return redirect('transactions:transaction_detail', entry.id)
```

## Responsive Design

The application is fully responsive across all device sizes:

### Breakpoints

| Device | Breakpoint | Layout Changes |
|--------|------------|----------------|
| **Desktop** | 1025px+ | Full layout, all columns visible |
| **Tablet** | 768px - 1024px | Adjusted grids, optimized spacing |
| **Mobile Landscape** | 577px - 768px | 2-column action buttons, single-column cards |
| **Mobile Portrait** | ≤576px | Hamburger menu, hidden non-essential columns |

### Mobile Features

**Navigation**:
- Hamburger menu toggle (☰) at ≤992px
- Collapsible menu with smooth transitions
- Stacked navigation links
- Hidden "Welcome" text on small screens

**Tables**:
- Horizontal scrolling with touch support (`-webkit-overflow-scrolling: touch`)
- Hidden columns on mobile (e.g., "Main Account", "View" link)
- Reduced font sizes and padding

**Forms & Cards**:
- Single-column layouts on mobile
- Flexible grid systems using CSS Grid
- Touch-friendly button sizes

### CSS Structure

```css
/* Desktop default styles */
.acas-nav-links { display: flex; }

/* Tablet (≤1024px) */
@media (max-width: 1024px) {
    .summary-cards { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
}

/* Mobile (≤768px) */
@media (max-width: 768px) {
    .acas-nav-links {
        flex-direction: column;
        max-height: 0;
        overflow: hidden;
    }
    .acas-nav-links.active { max-height: 500px; }
}

/* Small mobile (≤576px) */
@media (max-width: 576px) {
    .actions-grid { grid-template-columns: 1fr; }
}
```

## URL Configuration

### Main Routes

| URL | View | Purpose |
|-----|------|---------|
| `/` | `dashboard_view` | Landing page with financial summary |
| `/login/` | `login_view` | Custom authentication |
| `/logout/` | `logout_view` | Logout handler |
| `/accounts/` | `chart_of_accounts` | Trial balance view with 3-level hierarchy |
| `/accounts/<id>/` | `account_detail` | Transaction history for account |
| `/transactions/` | `transaction_list` | List all journal entries |
| `/transactions/new/` | `transaction_new` | Create journal entry (formset) |
| `/transactions/<id>/` | `transaction_detail` | View entry details |
| `/transactions/<id>/edit/` | `transaction_edit` | Edit draft entry |
| `/transactions/<id>/post/` | `transaction_post` | Post entry to ledger |
| `/transactions/<id>/unpost/` | `transaction_unpost` | Revert posting status |
| `/reports/` | `reports_index` | Reports menu |
| `/reports/balance-sheet/` | `balance_sheet` | Assets = Liabilities + Equity |
| `/reports/income-statement/` | `income_statement` | Revenue - Expenses |
| `/reports/trial-balance/` | `trial_balance` | All accounts with debit/credit |
| `/reports/cash-flow/` | `cash_flow` | Operating/Investing/Financing |
| `/settings/` | `settings_view` | Site settings (superuser only) |
| `/admin/` | Django Admin | Full admin interface (superuser only) |

## Utility Scripts

Located in project root for operational tasks:

### check_balance.py
Diagnostic script to verify ledger integrity:
```bash
python check_balance.py
```
**Checks**:
- Posted vs draft transaction counts
- Total debits vs total credits (must equal)
- Balance by account type
- Balance sheet equation: Assets = Liabilities + Equity
- Net income calculation
- Color-coded terminal output

### close_period.py
Create closing entries to zero revenue/expense accounts:
```bash
python close_period.py
```
**Process**:
1. Debit all revenue accounts (zero balances)
2. Credit all expense accounts (zero balances)
3. Transfer net income to "Current Year Earnings" (3101)
4. Validate entry is balanced
5. Post the closing entry automatically

**Requirements**: Sub-account 3101 must exist for retained earnings

### create_sample_data.py
Generate demo data for testing:
```bash
python create_sample_data.py
```

### reverse_closing.py
Reverse previously created closing entries:
```bash
python reverse_closing.py
```

## Access Control & Permissions

### User Roles

**Authenticated Users**:
- View dashboard, accounts, transactions, reports
- Create and edit journal entries
- Post/unpost transactions
- View chart of accounts

**Superusers Only**:
- Access Django Admin (`/admin/`)
- Manage site settings (`/settings/`)
- Create/edit MainAccount, AccountClass, SubAccount
- View Settings and Admin links in navigation
- Modify system configuration

### Implementation

```python
# Require authentication for all views
from django.contrib.auth.decorators import login_required

@login_required
def chart_of_accounts(request):
    # View logic

# Require superuser for administrative functions
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def settings_view(request):
    # Settings logic
```

### Navigation Display Logic

```django
<!-- Show admin links only for superusers -->
{% if user.is_superuser %}
<ul class="acas-nav-links acas-nav-admin">
    <li><a href="/settings">⚙️ Settings</a></li>
    <li><a href="/admin">🔧 Admin</a></li>
</ul>
{% endif %}
```

## Design System

### Color Palette (ACAS Theme)

```css
/* Primary Colors */
--acas-primary: #1a6473;          /* Teal - Navigation, primary actions */
--acas-primary-dark: #135260;     /* Dark teal - Hover states */
--acas-primary-light: #e6f3f5;    /* Light teal - Backgrounds */

/* Neutral Colors */
--acas-bg: #f8f9fa;               /* Page background */
--acas-surface: #ffffff;          /* Card/surface background */
--acas-border: #e2e8f0;           /* Borders */
--acas-text: #1a2a2a;             /* Primary text */
--acas-text-muted: #6b7280;       /* Secondary text */

/* Account Type Colors */
--asset-color: #1976d2;           /* Blue */
--liability-color: #d32f2f;       /* Red */
--equity-color: #388e3c;          /* Green */
--revenue-color: #7b1fa2;         /* Purple */
--expense-color: #f57c00;         /* Orange */
```

### Typography

- **Brand Font**: Georgia, 'Times New Roman', serif (company name)
- **Body Font**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Code Font**: 'Courier New', monospace (account codes, amounts)

### Component Styling

**Navigation Bar**:
- Teal background (#1a6473)
- Uppercase labels with letter-spacing
- Active state: white bottom border
- Sticky positioning at top

**Tables**:
- Trial balance format: debit/credit columns
- Color-coded type headers (by account type)
- Hover effects on rows
- Responsive horizontal scrolling

**Forms**:
- Bootstrap-style form controls
- Inline formsets for transaction lines
- Balance validation indicators

## Production Deployment Checklist

Before deploying to production:

1. **Environment Variables**:
   ```bash
   # Create .env file
   SECRET_KEY=your-secure-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

2. **Database Migration**:
   ```bash
   python manage.py migrate --settings=accounting_acas.settings_production
   ```

3. **Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Security Settings**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set secure `SECRET_KEY` (from environment variable)
   - Enable HTTPS with `SECURE_SSL_REDIRECT = True`
   - Set `CSRF_COOKIE_SECURE = True`
   - Set `SESSION_COOKIE_SECURE = True`

5. **Database**:
   - Switch to PostgreSQL (production-ready ACID compliance)
   - Configure database backups
   - Set up connection pooling

6. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Chart of Accounts**:
   ```bash
   python manage.py loaddata initial_data.json  # If available
   ```

## Common Development Tasks

### Adding a New Account

```python
# Via Django shell
python manage.py shell

from accounts.models import MainAccount, SubAccount, AccountType
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()

# Create Main Account
main = MainAccount.objects.create(
    code='1000',
    name='Cash',
    account_type=AccountType.ASSET,
    created_by=user,
    updated_by=user
)

# Create Sub-Account
sub = SubAccount.objects.create(
    code='1001',
    name='Cash on Hand',
    main_account=main,
    created_by=user,
    updated_by=user
)
```

### Creating a Journal Entry Programmatically

```python
from transactions.models import JournalEntry, TransactionLine
from accounts.models import SubAccount
from django.db import transaction
from decimal import Decimal

with transaction.atomic():
    # Create journal entry
    entry = JournalEntry.objects.create(
        entry_number='JE-2024-001',
        date='2024-01-15',
        description='Sample transaction',
        created_by=user,
        updated_by=user
    )

    # Add debit line
    TransactionLine.objects.create(
        journal_entry=entry,
        sub_account=cash_account,
        description='Cash received',
        debit=Decimal('1000.00'),
        credit=Decimal('0.00'),
        created_by=user,
        updated_by=user
    )

    # Add credit line
    TransactionLine.objects.create(
        journal_entry=entry,
        sub_account=revenue_account,
        description='Service revenue',
        debit=Decimal('0.00'),
        credit=Decimal('1000.00'),
        created_by=user,
        updated_by=user
    )

    # Validate and post
    if entry.is_balanced():
        entry.post(user)
```

## Troubleshooting

### Common Issues

**Issue**: "Debits must equal credits" error when saving journal entry
- **Solution**: Verify all transaction lines sum correctly. Use formset validation in admin/views.

**Issue**: Cannot edit journal entry
- **Solution**: Check if entry is posted. Unpost it first using the unpost view/action.

**Issue**: Balance sheet doesn't balance
- **Solution**: Run `python check_balance.py` to diagnose. Verify all posted entries are balanced.

**Issue**: 3-level hierarchy not showing for expenses
- **Solution**: Ensure AccountClass is created and linked to SubAccount via `account_class` ForeignKey.

**Issue**: Responsive menu not working on mobile
- **Solution**: Check browser console for JavaScript errors. Verify navbar.html script is included.
