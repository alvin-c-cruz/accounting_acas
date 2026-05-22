# Database Initialization on PythonAnywhere

This guide provides step-by-step instructions for initializing the database on PythonAnywhere for the Accounting System.

## Prerequisites

- PythonAnywhere account created
- Repository cloned to PythonAnywhere
- Virtual environment created and activated
- Dependencies installed from requirements.txt
- .env file configured with SECRET_KEY

## Step-by-Step Database Initialization

### 1. Open PythonAnywhere Bash Console

1. Log in to https://www.pythonanywhere.com
2. Go to **Consoles** tab
3. Click **Bash** to start a new bash console

### 2. Navigate to Project and Activate Environment

```bash
# Navigate to project directory
cd ~/accounting_acas

# Activate virtual environment
workon accounting_env

# Verify you're in the right place
pwd
# Should output: /home/alvinccruz/accounting_acas
```

### 3. Configure Environment Variables (.env file)

**IMPORTANT**: Create the .env file with production settings first!

```bash
# Create .env file
nano .env
```

Add the following content (press Ctrl+O to save, Ctrl+X to exit):

```env
# Generate SECRET_KEY first with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=alvinccruz.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://alvinccruz.pythonanywhere.com
```

**Generate SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and paste it into your .env file.

### 4. Run Database Migrations

```bash
# Check if migrations are ready
python manage.py showmigrations

# Apply all migrations
python manage.py migrate

# You should see output like:
# Operations to perform:
#   Apply all migrations: accounts, admin, auth, contenttypes, sessions, settings_app, transactions
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   [... more migrations ...]
```

### 5. Create Superuser Account

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Username**: Choose an admin username (e.g., `admin` or `alvinccruz`)
- **Email**: Your email address
- **Password**: Strong password (at least 8 characters)
- **Password (again)**: Confirm password

**IMPORTANT**: Remember these credentials! You'll need them to:
- Access Django Admin at https://alvinccruz.pythonanywhere.com/admin/
- Activate newly registered users

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput

# This copies CSS, JavaScript, and images to staticfiles/ directory
# You should see: "X static files copied to '/home/alvinccruz/accounting_acas/staticfiles'"
```

### 7. Choose Your Data Setup Path

You have two options:

---

#### **Option A: Production Setup (Real Company Data)**

For a real company, manually create your chart of accounts:

1. **Access Admin Panel**:
   - Go to https://alvinccruz.pythonanywhere.com/admin/
   - Log in with your superuser credentials

2. **Set Up Site Settings** (Required):
   - Go to **Site Settings** in admin
   - Add **Company Name** and **Copyright Text**
   - Click **Save**

3. **Create Account Structure**:

   **Step 1**: Create Account Types
   - Go to **Accounts → Account Types**
   - Create: Assets, Liabilities, Equity, Revenue, Expenses

   **Step 2**: Create Main Accounts
   - Go to **Accounts → Main Accounts**
   - Link each to an Account Type
   - Example:
     - Code: 1000, Name: "Current Assets", Type: Assets
     - Code: 2000, Name: "Current Liabilities", Type: Liabilities
     - Code: 3000, Name: "Equity", Type: Equity
     - Code: 4000, Name: "Operating Revenue", Type: Revenue
     - Code: 5000, Name: "Operating Expenses", Type: Expenses

   **Step 3**: Create Sub-Accounts (the actual accounts used in transactions)
   - Go to **Accounts → Sub Accounts**
   - Link each to a Main Account
   - Examples:
     - Code: 1001, Name: "Cash", Main Account: 1000
     - Code: 1002, Name: "Accounts Receivable", Main Account: 1000
     - Code: 2001, Name: "Accounts Payable", Main Account: 2000
     - Code: 3101, Name: "Current Year Earnings", Main Account: 3000 (REQUIRED for period closing)
     - Code: 4001, Name: "Sales Revenue", Main Account: 4000
     - Code: 5001, Name: "Salaries Expense", Main Account: 5000

   **Step 4**: (Optional) Create Account Classes for Expense Categorization
   - Go to **Accounts → Account Classes**
   - Create: Cost of Goods Sold, Selling Expenses, Administrative Expenses
   - Assign expense sub-accounts to appropriate classes

4. **Verify Setup**:
   - Go to your app: https://alvinccruz.pythonanywhere.com
   - Click **Chart of Accounts** (Trial Balance)
   - You should see your account structure with zero balances

---

#### **Option B: Development/Demo Setup (Sample Data)**

For testing or demonstration purposes, use the sample data scripts:

```bash
# Make sure you're in the project directory with virtualenv activated
cd ~/accounting_acas
workon accounting_env

# Create sample chart of accounts (3-level hierarchy)
python scripts/create_sample_data.py

# Expected output:
# Creating sample data...
# ✓ Created account types
# ✓ Created main accounts
# ✓ Created account classes
# ✓ Created sub-accounts
# Sample data created successfully!

# (Optional) Create sample transactions for testing reports
python scripts/create_sample_transactions.py

# Expected output:
# Creating sample transactions...
# ✓ Created X journal entries
# Sample transactions created successfully!
```

**What gets created:**
- Complete 3-level account hierarchy (Account Types → Main Accounts → Sub-Accounts)
- Account classes for expense categorization
- Sample transactions (if you run the second script)

---

### 8. Verify Database Initialization

```bash
# Check database integrity
python scripts/check_balance.py

# You should see:
# ✓ Total debits equal total credits
# ✓ Balance sheet equation balanced
# (or zero balances if no transactions yet)
```

### 9. Test the Application

1. Visit: https://alvinccruz.pythonanywhere.com
2. Log in with your superuser credentials
3. Check:
   - Dashboard loads correctly
   - Chart of Accounts shows your accounts
   - You can create transactions
   - Reports generate (may be empty if no transactions)

---

## Post-Initialization Tasks

### Activate Registered Users (Admin Approval Workflow)

When new users register:

1. Go to https://alvinccruz.pythonanywhere.com/admin/
2. Click **Users** under **Authentication and Authorization**
3. Find users with ❌ (inactive status)
4. **Option 1**: Click on username → Check **Active** → Click **Save**
5. **Option 2**: Select multiple users → Choose **"Activate selected users"** action → Click **Go**

### Create Additional Admin Users

If you need more admin users:

```bash
cd ~/accounting_acas
workon accounting_env
python manage.py createsuperuser
```

Or promote existing users in Django Admin:
1. Go to Users
2. Click on username
3. Check **Staff status** (to access admin)
4. Check **Superuser status** (for full permissions)
5. Click **Save**

---

## Troubleshooting

### Migration Errors

**Error**: `No migrations to apply`
- This is normal if database is already initialized

**Error**: `django.db.utils.OperationalError: no such table`
- Run: `python manage.py migrate`

**Error**: `ImproperlyConfigured: Requested setting SECRET_KEY`
- Check that .env file exists with SECRET_KEY
- Verify python-decouple is installed: `pip list | grep decouple`

### Static Files Not Loading

```bash
cd ~/accounting_acas
workon accounting_env
python manage.py collectstatic --noinput
```

Then reload web app from PythonAnywhere Web tab.

### Can't Access Admin Panel

1. Verify superuser exists:
   ```bash
   python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).count())"
   ```
2. If output is `0`, create superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Database Locked Errors

SQLite doesn't handle concurrent writes well. If you get "database is locked":
1. Make sure no other processes are accessing the database
2. Reload the web app
3. Consider upgrading to MySQL (paid PythonAnywhere tier)

---

## Database Backup

### Manual Backup

```bash
# In PythonAnywhere bash console
cd ~/accounting_acas
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d)

# Verify backup
ls -lh db.sqlite3*
```

### Download Backup to Local Machine

1. Go to **Files** tab in PythonAnywhere
2. Navigate to `/home/alvinccruz/accounting_acas/`
3. Click on `db.sqlite3` → **Download**

### Restore from Backup

```bash
cd ~/accounting_acas
cp db.sqlite3.backup-YYYYMMDD db.sqlite3

# Reload web app
touch /var/www/alvinccruz_pythonanywhere_com_wsgi.py
```

---

## Database Maintenance

### Check Database Integrity

```bash
cd ~/accounting_acas
workon accounting_env
python scripts/check_balance.py
```

### Period Closing

```bash
# Close accounting period (transfer revenue/expenses to equity)
python scripts/close_period.py

# Reverse if needed
python scripts/reverse_closing.py
```

---

## Quick Reference Commands

```bash
# Navigate and activate
cd ~/accounting_acas
workon accounting_env

# Database operations
python manage.py migrate                    # Apply migrations
python manage.py makemigrations             # Create new migrations (after model changes)
python manage.py showmigrations             # Show migration status
python manage.py createsuperuser            # Create admin user

# Data operations
python scripts/create_sample_data.py        # Create sample chart of accounts
python scripts/create_sample_transactions.py # Create sample transactions
python scripts/check_balance.py             # Verify data integrity

# Static files
python manage.py collectstatic --noinput    # Collect static files

# Database backup
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d)

# Reload web app (after changes)
touch /var/www/alvinccruz_pythonanywhere_com_wsgi.py
```

---

## Summary

**Minimum Required Steps**:
1. ✅ Create .env file with SECRET_KEY
2. ✅ Run migrations: `python manage.py migrate`
3. ✅ Create superuser: `python manage.py createsuperuser`
4. ✅ Collect static files: `python manage.py collectstatic --noinput`
5. ✅ Create chart of accounts (manually or via script)
6. ✅ Reload web app

**Your database is now initialized and ready to use!**

For updates and maintenance, see [DEPLOYMENT_PYTHONANYWHERE.md](DEPLOYMENT_PYTHONANYWHERE.md).
