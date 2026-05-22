from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import SiteSettings


@user_passes_test(lambda u: u.is_superuser)
def settings_view(request):
    """
    Custom settings page for superusers only to edit site settings
    """
    settings = SiteSettings.get_settings()

    if request.method == 'POST':
        # Update settings from form
        settings.company_name = request.POST.get('company_name', settings.company_name)
        settings.copyright_text = request.POST.get('copyright_text', settings.copyright_text)
        settings.save()

        messages.success(request, 'Settings updated successfully!')
        return redirect('settings_app:settings')

    context = {
        'settings': settings,
    }
    return render(request, 'settings_app/settings.html', context)


def login_view(request):
    """
    Custom login view with account activation check
    """
    if request.user.is_authenticated:
        # Check if user is active
        if not request.user.is_active:
            return redirect('settings_app:pending_approval')
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate without is_active check
        from django.contrib.auth.backends import ModelBackend
        backend = ModelBackend()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # User credentials are correct, check if active
                if not user.is_active:
                    messages.warning(request, 'Your account is pending admin approval. Please wait for activation.')
                    return render(request, 'settings_app/pending_approval.html')

                # User is active, log them in
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'settings_app/login.html')


def register_view(request):
    """
    User registration view - creates inactive accounts by default
    """
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'settings_app/register.html')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'settings_app/register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'settings_app/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'settings_app/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'settings_app/register.html')

        # Create inactive user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # Inactive by default
        )

        messages.success(request, 'Registration successful! Your account is pending admin approval.')
        return redirect('settings_app:pending_approval')

    return render(request, 'settings_app/register.html')


def pending_approval_view(request):
    """
    Page shown to users whose accounts are pending approval
    """
    return render(request, 'settings_app/pending_approval.html')


@login_required
def logout_view(request):
    """
    Custom logout view that handles both GET and POST
    """
    logout(request)
    return redirect('login')
