from django.db import models


class SiteSettings(models.Model):
    """
    Site-wide settings that can be configured by superuser.
    Only one instance should exist.
    """
    company_name = models.CharField(
        max_length=200,
        default='Alvin Cruz Accounting Services',
        help_text='Company name displayed in header and title'
    )

    copyright_text = models.CharField(
        max_length=200,
        default='Alvin Cruz Accounting Services. All rights reserved.',
        help_text='Copyright text displayed in footer'
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f'Site Settings - {self.company_name}'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton pattern)
        if not self.pk and SiteSettings.objects.exists():
            # If trying to create a new instance when one exists, update the existing one
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get the site settings instance, create if doesn't exist"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
