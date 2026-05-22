from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout, authenticate, login
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
    Custom login view
    """
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'settings_app/login.html')


@login_required
def logout_view(request):
    """
    Custom logout view that handles both GET and POST
    """
    logout(request)
    return redirect('login')
