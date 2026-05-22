"""
Context processors to make site settings available in all templates
"""
from .models import SiteSettings


def site_settings(request):
    """
    Add site settings to template context
    """
    settings = SiteSettings.get_settings()
    return {
        'site_settings': settings,
    }
