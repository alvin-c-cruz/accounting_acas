from django.contrib import admin
from django.utils.html import format_html
from .models import MainAccount, SubAccount, AccountClass


class SubAccountInline(admin.TabularInline):
    """
    Inline admin to display and manage sub-accounts within the MainAccount admin page.
    This allows users to see and edit sub-accounts directly from the main account page.
    """
    model = SubAccount
    extra = 1
    fields = ['code', 'name', 'account_class', 'description', 'is_active']
    ordering = ['code']
    autocomplete_fields = ['account_class']


@admin.register(MainAccount)
class MainAccountAdmin(admin.ModelAdmin):
    """
    Admin interface for Main Accounts with enhanced display and filtering.
    Shows sub-accounts inline for easy management.
    """
    list_display = [
        'code',
        'name',
        'account_type',
        'sub_accounts_count',
        'balance_display',
        'is_active',
        'created_at'
    ]
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    fieldsets = (
        ('Account Information', {
            'fields': ('code', 'name', 'account_type', 'description', 'is_active')
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    inlines = [SubAccountInline]

    def sub_accounts_count(self, obj):
        """Display the number of sub-accounts"""
        count = obj.sub_accounts.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #e3f2fd; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">{}</span>',
                count
            )
        return '0'
    sub_accounts_count.short_description = 'Sub-Accounts'

    def balance_display(self, obj):
        """Display the current balance with currency formatting"""
        balance = obj.get_balance()
        color = '#2e7d32' if balance >= 0 else '#c62828'
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:,.2f}</span>',
            color,
            balance
        )
    balance_display.short_description = 'Balance'

    def save_model(self, request, obj, form, change):
        """Automatically set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Set user for inline sub-accounts"""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:  # New object
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        formset.save_m2m()


@admin.register(SubAccount)
class SubAccountAdmin(admin.ModelAdmin):
    """
    Admin interface for Sub Accounts with filtering and search capabilities.
    """
    list_display = [
        'code',
        'name',
        'main_account',
        'account_class',
        'account_type_display',
        'balance_display',
        'is_active',
        'created_at'
    ]
    list_filter = ['main_account__account_type', 'account_class', 'is_active', 'created_at', 'main_account']
    search_fields = ['code', 'name', 'description', 'main_account__name', 'account_class__name']
    ordering = ['code']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['main_account', 'account_class']

    fieldsets = (
        ('Account Information', {
            'fields': ('main_account', 'account_class', 'code', 'name', 'description', 'is_active')
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def account_type_display(self, obj):
        """Display the account type from parent main account"""
        type_colors = {
            'ASSET': '#1976d2',
            'LIABILITY': '#d32f2f',
            'EQUITY': '#388e3c',
            'REVENUE': '#7b1fa2',
            'EXPENSE': '#f57c00',
        }
        account_type = obj.account_type
        color = type_colors.get(account_type, '#666')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.main_account.get_account_type_display()
        )
    account_type_display.short_description = 'Account Type'

    def balance_display(self, obj):
        """Display the current balance with currency formatting"""
        balance = obj.get_balance()
        color = '#2e7d32' if balance >= 0 else '#c62828'
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:,.2f}</span>',
            color,
            balance
        )
    balance_display.short_description = 'Balance'

    def save_model(self, request, obj, form, change):
        """Automatically set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AccountClass)
class AccountClassAdmin(admin.ModelAdmin):
    """
    Admin interface for Account Classes (e.g., COGS, Selling Expenses, Administrative Expenses).
    """
    list_display = [
        'code',
        'name',
        'main_account',
        'sub_accounts_count',
        'balance_display',
        'is_active',
        'created_at'
    ]
    list_filter = ['main_account', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'description', 'main_account__name']
    ordering = ['code']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['main_account']

    fieldsets = (
        ('Class Information', {
            'fields': ('main_account', 'code', 'name', 'description', 'is_active')
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def sub_accounts_count(self, obj):
        """Display the number of sub-accounts in this class"""
        count = obj.sub_accounts.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #e3f2fd; padding: 3px 8px; '
                'border-radius: 3px; font-weight: bold;">{}</span>',
                count
            )
        return '0'
    sub_accounts_count.short_description = 'Sub-Accounts'

    def balance_display(self, obj):
        """Display the current balance with currency formatting"""
        balance = obj.get_balance()
        color = '#2e7d32' if balance >= 0 else '#c62828'
        return format_html(
            '<span style="color: {}; font-weight: bold;">${:,.2f}</span>',
            color,
            balance
        )
    balance_display.short_description = 'Balance'

    def save_model(self, request, obj, form, change):
        """Automatically set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# Customize the admin site header and title
admin.site.site_header = 'Accounting System Administration'
admin.site.site_title = 'Accounting Admin'
admin.site.index_title = 'Welcome to Accounting System Administration'
