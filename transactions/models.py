from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from accounts.models import BaseModel, SubAccount


class JournalEntry(BaseModel):
    """
    Journal Entry represents a complete accounting transaction.
    Each entry must have balanced debits and credits (double-entry bookkeeping).
    """
    entry_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique journal entry number (e.g., JE-2024-001)"
    )
    date = models.DateField(
        default=timezone.now,
        help_text="Transaction date"
    )
    description = models.TextField(
        help_text="Description of the transaction"
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="External reference number (invoice, receipt, etc.)"
    )
    is_posted = models.BooleanField(
        default=False,
        help_text="Whether this entry has been posted to the ledger"
    )
    posted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the entry was posted"
    )

    class Meta:
        ordering = ['-date', '-entry_number']
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'

    def __str__(self):
        return f"{self.entry_number} - {self.date} - {self.description[:50]}"

    def get_total_debits(self):
        """Calculate total debits for this journal entry"""
        total = self.lines.aggregate(
            total=models.Sum('debit', default=Decimal('0'))
        )['total']
        return total or Decimal('0.00')

    def get_total_credits(self):
        """Calculate total credits for this journal entry"""
        total = self.lines.aggregate(
            total=models.Sum('credit', default=Decimal('0'))
        )['total']
        return total or Decimal('0.00')

    def is_balanced(self):
        """Check if debits equal credits"""
        return self.get_total_debits() == self.get_total_credits()

    def clean(self):
        """Validate the journal entry before saving"""
        super().clean()

        # Only validate balance if the entry has lines
        if self.pk:  # Entry already exists, can check lines
            if not self.is_balanced():
                raise ValidationError(
                    f"Journal entry must be balanced. "
                    f"Debits: ${self.get_total_debits()}, "
                    f"Credits: ${self.get_total_credits()}"
                )

    def post(self, user=None):
        """
        Post the journal entry to the ledger.
        Once posted, the entry should not be modified.
        """
        if self.is_posted:
            raise ValidationError("This entry has already been posted.")

        if not self.is_balanced():
            raise ValidationError("Cannot post an unbalanced entry.")

        if self.lines.count() < 2:
            raise ValidationError("A journal entry must have at least 2 lines.")

        self.is_posted = True
        self.posted_at = timezone.now()
        if user:
            self.updated_by = user
        self.save()

    def unpost(self, user=None):
        """Unpost the journal entry (for corrections)"""
        if not self.is_posted:
            raise ValidationError("This entry is not posted.")

        self.is_posted = False
        self.posted_at = None
        if user:
            self.updated_by = user
        self.save()


class TransactionLine(BaseModel):
    """
    Individual line items within a Journal Entry.
    Each line represents a debit or credit to a specific sub-account.
    """
    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='lines',
        help_text="Parent journal entry"
    )
    sub_account = models.ForeignKey(
        SubAccount,
        on_delete=models.PROTECT,
        related_name='transaction_lines',
        help_text="Sub-account affected by this transaction"
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        help_text="Description for this specific line"
    )
    debit = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Debit amount"
    )
    credit = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Credit amount"
    )

    class Meta:
        ordering = ['journal_entry', 'id']
        verbose_name = 'Transaction Line'
        verbose_name_plural = 'Transaction Lines'

    def __str__(self):
        account_name = f"{self.sub_account.code} - {self.sub_account.name}"
        if self.debit > 0:
            return f"{account_name} - Debit: ${self.debit}"
        else:
            return f"{account_name} - Credit: ${self.credit}"

    def clean(self):
        """Validate the transaction line before saving"""
        super().clean()

        # A line must have either a debit OR a credit, but not both
        if self.debit > 0 and self.credit > 0:
            raise ValidationError("A transaction line cannot have both debit and credit amounts.")

        # A line must have at least one non-zero amount
        if self.debit == 0 and self.credit == 0:
            raise ValidationError("A transaction line must have either a debit or credit amount.")

        # Amounts cannot be negative
        if self.debit < 0 or self.credit < 0:
            raise ValidationError("Debit and credit amounts cannot be negative.")

    def save(self, *args, **kwargs):
        """Override save to run validations"""
        self.clean()
        super().save(*args, **kwargs)

    @property
    def amount(self):
        """Return the non-zero amount (either debit or credit)"""
        return self.debit if self.debit > 0 else self.credit

    @property
    def transaction_type(self):
        """Return whether this is a debit or credit transaction"""
        return 'Debit' if self.debit > 0 else 'Credit'
