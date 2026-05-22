from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import JournalEntry, TransactionLine


class TransactionLineInline(admin.TabularInline):
    """
    Inline admin to display and manage transaction lines within the JournalEntry admin page.
    """
    model = TransactionLine
    extra = 2
    fields = ['sub_account', 'description', 'debit', 'credit']
    autocomplete_fields = ['sub_account']

    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly if journal entry is posted"""
        if obj and obj.is_posted:
            return ['sub_account', 'description', 'debit', 'credit']
        return []


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    """
    Admin interface for Journal Entries with inline transaction lines.
    Includes validation for double-entry bookkeeping.
    """
    list_display = [
        'entry_number',
        'date',
        'description_short',
        'total_debits_display',
        'total_credits_display',
        'balanced_status',
        'post_status',
        'created_at'
    ]
    list_filter = ['is_posted', 'date', 'created_at']
    search_fields = ['entry_number', 'description', 'reference']
    ordering = ['-date', '-entry_number']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by', 'posted_at']

    fieldsets = (
        ('Journal Entry Information', {
            'fields': ('entry_number', 'date', 'description', 'reference')
        }),
        ('Posting Status', {
            'fields': ('is_posted', 'posted_at')
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    inlines = [TransactionLineInline]

    actions = ['post_entries', 'unpost_entries']

    def get_readonly_fields(self, request, obj=None):
        """Make most fields readonly if journal entry is posted"""
        readonly = list(self.readonly_fields)
        if obj and obj.is_posted:
            readonly.extend(['entry_number', 'date', 'description', 'reference'])
        return readonly

    def description_short(self, obj):
        """Display shortened description"""
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description
    description_short.short_description = 'Description'

    def total_debits_display(self, obj):
        """Display total debits with currency formatting"""
        total = obj.get_total_debits()
        return format_html(
            '<span style="color: #1976d2; font-weight: bold;">${:,.2f}</span>',
            total
        )
    total_debits_display.short_description = 'Total Debits'

    def total_credits_display(self, obj):
        """Display total credits with currency formatting"""
        total = obj.get_total_credits()
        return format_html(
            '<span style="color: #d32f2f; font-weight: bold;">${:,.2f}</span>',
            total
        )
    total_credits_display.short_description = 'Total Credits'

    def balanced_status(self, obj):
        """Display whether the entry is balanced"""
        is_balanced = obj.is_balanced()
        if is_balanced:
            return format_html(
                '<span style="background-color: #c8e6c9; color: #2e7d32; '
                'padding: 3px 8px; border-radius: 3px; font-weight: bold;">BALANCED</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #ffcdd2; color: #c62828; '
                'padding: 3px 8px; border-radius: 3px; font-weight: bold;">UNBALANCED</span>'
            )
    balanced_status.short_description = 'Status'

    def post_status(self, obj):
        """Display posting status"""
        if obj.is_posted:
            return format_html(
                '<span style="background-color: #e3f2fd; color: #1976d2; '
                'padding: 3px 8px; border-radius: 3px; font-weight: bold;">POSTED</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #fff3e0; color: #f57c00; '
                'padding: 3px 8px; border-radius: 3px; font-weight: bold;">DRAFT</span>'
            )
    post_status.short_description = 'Posting'

    def save_model(self, request, obj, form, change):
        """Automatically set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Set user for inline transaction lines"""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:  # New object
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        formset.save_m2m()

        # After saving lines, validate balance
        obj = form.instance
        if obj.pk and not obj.is_balanced():
            messages.warning(
                request,
                f'Warning: Journal entry is unbalanced. '
                f'Debits: ${obj.get_total_debits()}, Credits: ${obj.get_total_credits()}'
            )

    def post_entries(self, request, queryset):
        """Action to post selected journal entries"""
        posted_count = 0
        error_count = 0

        for entry in queryset:
            try:
                entry.post(user=request.user)
                posted_count += 1
            except ValidationError as e:
                error_count += 1
                messages.error(request, f'{entry.entry_number}: {e.message}')

        if posted_count:
            messages.success(request, f'Successfully posted {posted_count} journal entry(ies).')
        if error_count:
            messages.warning(request, f'{error_count} entry(ies) could not be posted.')

    post_entries.short_description = 'Post selected journal entries'

    def unpost_entries(self, request, queryset):
        """Action to unpost selected journal entries"""
        unposted_count = 0
        error_count = 0

        for entry in queryset:
            try:
                entry.unpost(user=request.user)
                unposted_count += 1
            except ValidationError as e:
                error_count += 1
                messages.error(request, f'{entry.entry_number}: {e.message}')

        if unposted_count:
            messages.success(request, f'Successfully unposted {unposted_count} journal entry(ies).')
        if error_count:
            messages.warning(request, f'{error_count} entry(ies) could not be unposted.')

    unpost_entries.short_description = 'Unpost selected journal entries'


@admin.register(TransactionLine)
class TransactionLineAdmin(admin.ModelAdmin):
    """
    Admin interface for Transaction Lines.
    """
    list_display = [
        'journal_entry',
        'sub_account',
        'account_type_display',
        'debit_display',
        'credit_display',
        'created_at'
    ]
    list_filter = [
        'journal_entry__is_posted',
        'sub_account__main_account__account_type',
        'journal_entry__date',
        'created_at'
    ]
    search_fields = [
        'journal_entry__entry_number',
        'sub_account__code',
        'sub_account__name',
        'description'
    ]
    ordering = ['-journal_entry__date', 'journal_entry', 'id']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    autocomplete_fields = ['journal_entry', 'sub_account']

    fieldsets = (
        ('Transaction Information', {
            'fields': ('journal_entry', 'sub_account', 'description')
        }),
        ('Amounts', {
            'fields': ('debit', 'credit')
        }),
        ('Audit Information', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make fields readonly if parent journal entry is posted"""
        readonly = list(self.readonly_fields)
        if obj and obj.journal_entry.is_posted:
            readonly.extend(['journal_entry', 'sub_account', 'description', 'debit', 'credit'])
        return readonly

    def account_type_display(self, obj):
        """Display the account type from parent main account"""
        type_colors = {
            'ASSET': '#1976d2',
            'LIABILITY': '#d32f2f',
            'EQUITY': '#388e3c',
            'REVENUE': '#7b1fa2',
            'EXPENSE': '#f57c00',
        }
        account_type = obj.sub_account.account_type
        color = type_colors.get(account_type, '#666')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.sub_account.main_account.get_account_type_display()
        )
    account_type_display.short_description = 'Account Type'

    def debit_display(self, obj):
        """Display debit amount"""
        if obj.debit > 0:
            return format_html(
                '<span style="color: #1976d2; font-weight: bold;">${:,.2f}</span>',
                obj.debit
            )
        return '-'
    debit_display.short_description = 'Debit'

    def credit_display(self, obj):
        """Display credit amount"""
        if obj.credit > 0:
            return format_html(
                '<span style="color: #d32f2f; font-weight: bold;">${:,.2f}</span>',
                obj.credit
            )
        return '-'
    credit_display.short_description = 'Credit'

    def save_model(self, request, obj, form, change):
        """Automatically set created_by and updated_by fields"""
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
