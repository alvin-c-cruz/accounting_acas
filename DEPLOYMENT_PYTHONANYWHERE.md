# Deploying to PythonAnywhere

This guide will help you deploy the Django Accounting System to PythonAnywhere.

## Prerequisites

1. **PythonAnywhere Account**: Sign up at https://www.pythonanywhere.com
   - Free tier: `alvinccruz.pythonanywhere.com`
   - Paid tier: Custom domain support

2. **GitHub Repository**: Code already pushed to https://github.com/alvin-c-cruz/accounting_acas

## Deployment Steps

### Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Sign up for an account (Free or Paid)
3. Log in to your dashboard

### Step 2: Clone Repository

Open a **Bash console** in PythonAnywhere:

```bash
# Clone your repository
git clone https://github.com/alvin-c-cruz/accounting_acas.git

# Navigate to project directory
cd accounting_acas

# Verify files
ls -la
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment with Python 3.10 or 3.11
mkvirtualenv --python=/usr/bin/python3.10 accounting_env

# Activate virtual environment (should auto-activate after creation)
workon accounting_env

# Install dependencies
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn whitenoise
```

### Step 4: Configure Environment Variables

Create `.env` file in the project root:

```bash
# In PythonAnywhere bash console
cd ~/accounting_acas
nano .env
```

Add these variables:

```env
# Django Secret Key (generate a new one!)
SECRET_KEY=your-very-long-random-secret-key-here

# Debug (MUST be False in production)
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=alvinccruz.pythonanywhere.com

# Database (if using PostgreSQL)
# DATABASE_URL=postgresql://user:password@host:port/dbname

# Static files
STATIC_ROOT=/home/alvinccruz/accounting_acas/staticfiles
STATIC_URL=/static/

# Media files
MEDIA_ROOT=/home/alvinccruz/accounting_acas/media
MEDIA_URL=/media/
```

**Generate a new SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Update Django Settings

Edit `accounting_acas/settings.py` to use environment variables:

```python
import os
from pathlib import Path
from decouple import config

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database (use SQLite for PythonAnywhere free tier)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Add WhiteNoise middleware for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # PythonAnywhere handles SSL
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

### Step 6: Run Migrations

```bash
# Navigate to project directory
cd ~/accounting_acas

# Activate virtual environment
workon accounting_env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Configure Web App in PythonAnywhere

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (NOT Django)
4. Choose **Python 3.10** (or 3.11)

#### Configure WSGI file:

Click on the **WSGI configuration file** link and replace contents with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/alvinccruz/accounting_acas'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'accounting_acas.settings'

# Activate virtual environment
from pathlib import Path
activate_this = '/home/alvinccruz/.virtualenvs/accounting_env/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `alvinccruz` with your actual PythonAnywhere username!**

#### Configure Virtual Environment:

In the **Virtualenv** section:
- Enter: `/home/alvinccruz/.virtualenvs/accounting_env`

#### Configure Static Files:

In the **Static files** section, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/alvinccruz/accounting_acas/staticfiles/` |
| `/media/` | `/home/alvinccruz/accounting_acas/media/` |

#### Configure Source Code:

In the **Code** section:
- **Source code**: `/home/alvinccruz/accounting_acas`
- **Working directory**: `/home/alvinccruz/accounting_acas`

### Step 8: Reload Web App

1. Click the **Reload** button (big green button)
2. Visit your site: `https://alvinccruz.pythonanywhere.com`

## Post-Deployment

### Create Initial Data

```bash
# SSH into PythonAnywhere or use bash console
cd ~/accounting_acas
workon accounting_env

# Create sample data (optional)
python scripts/create_sample_data.py
python scripts/create_sample_transactions.py
```

### Access Admin Panel

1. Go to `https://alvinccruz.pythonanywhere.com/admin/`
2. Log in with superuser credentials
3. Create MainAccounts, AccountClasses, and SubAccounts

## Updating the Application

When you make changes and push to GitHub:

```bash
# In PythonAnywhere bash console
cd ~/accounting_acas
workon accounting_env

# Pull latest changes
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Run migrations (if any)
python manage.py migrate

# Collect static files (if CSS/JS changed)
python manage.py collectstatic --noinput

# Reload web app (from Web tab or command line)
touch /var/www/alvinccruz_pythonanywhere_com_wsgi.py
```

Or simply click **Reload** in the Web tab.

## Database Backup

### SQLite Backup (Free Tier)

```bash
# Backup database
cd ~/accounting_acas
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d)

# Download backup via Files tab in PythonAnywhere
```

### PostgreSQL Backup (Paid Tier)

```bash
# If using PostgreSQL
pg_dump dbname > backup-$(date +%Y%m%d).sql
```

## Monitoring & Logs

### View Error Logs

1. Go to **Web** tab
2. Scroll to **Log files** section
3. Click on **Error log** or **Server log**

### Common Issues

**Issue**: Static files not loading
- **Solution**: Run `python manage.py collectstatic --noinput` and reload app

**Issue**: 502 Bad Gateway
- **Solution**: Check error log. Usually WSGI configuration or import error

**Issue**: Can't connect to database
- **Solution**: Check database path in settings.py and ensure migrations ran

**Issue**: CSRF verification failed
- **Solution**: Add your domain to `CSRF_TRUSTED_ORIGINS` in settings.py:
  ```python
  CSRF_TRUSTED_ORIGINS = ['https://alvinccruz.pythonanywhere.com']
  ```

## Security Checklist

Before going live:

- [ ] `DEBUG = False` in settings.py or .env
- [ ] Generate new `SECRET_KEY` (don't use default)
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Run `python manage.py check --deploy`
- [ ] Enable HTTPS (automatic on PythonAnywhere)
- [ ] Set secure cookie flags (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- [ ] Create strong superuser password
- [ ] Review Django security checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

## Performance Optimization

### Enable Compression (WhiteNoise)

Already configured with `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

### Database Optimization

```python
# In settings.py for SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}
```

### Caching (Optional)

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

## Free Tier Limitations

- CPU seconds per day: Limited
- Storage: 512MB
- MySQL database: 500MB
- One web app
- No custom domain (use `alvinccruz.pythonanywhere.com`)
- Console sessions timeout after inactivity

## Upgrade to Paid Tier

Benefits:
- More CPU seconds
- More storage
- PostgreSQL support
- Custom domains
- Always-on tasks
- SSH access

## Resources

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Django Deployment Docs**: https://docs.djangoproject.com/en/5.0/howto/deployment/
- **PythonAnywhere Django Tutorial**: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- **WhiteNoise Documentation**: http://whitenoise.evans.io/

## Support

If you encounter issues:

1. Check PythonAnywhere error logs (Web tab → Log files)
2. Check Django check: `python manage.py check --deploy`
3. PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
4. Django Documentation: https://docs.djangoproject.com/

---

**Your Django Accounting System is now live on PythonAnywhere!** 🎉

Access it at: `https://alvinccruz.pythonanywhere.com`
