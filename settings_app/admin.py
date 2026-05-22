from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'updated_at']
    fieldsets = (
        ('Company Information', {
            'fields': ('company_name',)
        }),
        ('Footer Settings', {
            'fields': ('copyright_text',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deleting the settings
        return False
