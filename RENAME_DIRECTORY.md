# Renaming the Project Directory

The Django project has been renamed from `accounting_ai` to `accounting_acas`.

## What's Been Updated

All internal references have been updated:
- ✅ Project directory: `accounting_ai/` → `accounting_acas/`
- ✅ `manage.py`
- ✅ `settings.py`
- ✅ `wsgi.py`
- ✅ `asgi.py`
- ✅ `urls.py`
- ✅ `CLAUDE.md`
- ✅ `README.md`

## Renaming the Root Directory

Since we're currently working inside the directory `c:\envs\accounting_ai`, you'll need to rename the outer directory from outside of it.

### Steps to Rename the Root Directory:

1. **Close this editor/IDE session**

2. **Navigate to the parent directory**:
   ```bash
   cd c:\envs
   ```

3. **Rename the directory**:
   ```bash
   # Windows Command Prompt:
   rename accounting_ai accounting_acas

   # Or PowerShell:
   Rename-Item accounting_ai accounting_acas

   # Or Git Bash:
   mv accounting_ai accounting_acas
   ```

4. **Navigate into the renamed directory**:
   ```bash
   cd accounting_acas
   ```

5. **Verify everything works**:
   ```bash
   python manage.py check
   python manage.py runserver
   ```

## That's It!

Your project is now fully renamed to `accounting_acas`.
