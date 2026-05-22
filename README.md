# Accounting System

A Django-based accounting system for managing financial transactions, accounts, and reports.

## Features

- Dashboard with financial summary
- Chart of accounts management
- Journal entries and transactions
- Financial reports (Balance Sheet, Income Statement, etc.)
- Django Admin interface for data management
- User authentication and permissions

## Getting Started

### Prerequisites

- Python 3.11+
- pip
- Virtual environment (recommended)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Unix/MacOS:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application:
- Dashboard: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Project Structure

- `accounting_acas/` - Project configuration
- `dashboard/` - Main dashboard app
- `accounts/` - Chart of accounts management
- `transactions/` - Transaction and journal entry management
- `reports/` - Financial reports
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, images

## Default Credentials

After creating a superuser, use those credentials to log in.

If you created the default superuser:
- Username: admin
- Password: (set during createsuperuser command)

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines and architecture information.

## Next Steps

1. Implement account models in the `accounts` app
2. Create transaction models with double-entry validation
3. Build financial reports
4. Add forms for data entry
5. Customize Django Admin for accounting workflows
