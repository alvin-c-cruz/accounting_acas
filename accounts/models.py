from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal


class BaseModel(models.Model):
    """
    Abstract base model with audit fields for tracking creation and modifications.
    All models should inherit from this to maintain audit trail.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class AccountType(models.TextChoices):
    """
    Five fundamental account types in accounting.
    - Assets: Resources owned by the business (normal debit balance)
    - Liabilities: Obligations owed to others (normal credit balance)
    - Equity: Owner's stake in the business (normal credit balance)
    - Revenue: Income from business operations (normal credit balance)
    - Expense: Costs of doing business (normal debit balance)
    """
    ASSET = 'ASSET', 'Asset'
    LIABILITY = 'LIABILITY', 'Liability'
    EQUITY = 'EQUITY', 'Equity'
    REVENUE = 'REVENUE', 'Revenue'
    EXPENSE = 'EXPENSE', 'Expense'


class AccountClass(BaseModel):
    """
    Account Classes for better categorization (middle layer).
    Used primarily for Expense accounts to categorize into:
    - Cost of Goods Sold
    - Selling Expenses
    - Administrative Expenses
    - Interest Expense
    Can also be used for other account types if needed.
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique class code (e.g., COGS, SELL, ADMIN, INT)"
    )
    name = models.CharField(
        max_length=200,
        help_text="Class name (e.g., Cost of Goods Sold, Selling Expenses)"
    )
    main_account = models.ForeignKey(
        'MainAccount',
        on_delete=models.PROTECT,
        related_name='account_classes',
        help_text="Parent main account"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this account class"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this class is currently active"
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Account Class'
        verbose_name_plural = 'Account Classes'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_balance(self):
        """
        Calculate the total balance of this account class by summing all sub-accounts.
        """
        total = Decimal('0.00')
        for sub_account in self.sub_accounts.filter(is_active=True):
            total += sub_account.get_balance()
        return total

    def clean(self):
        """Validation before saving"""
        super().clean()
        if self.code:
            self.code = self.code.strip().upper()


class MainAccount(BaseModel):
    """
    Main Account categories directly linked to Account Types.
    Examples:
    - Asset Type: Cash, Accounts Receivable, Inventory, Fixed Assets
    - Liability Type: Accounts Payable, Loans Payable
    - Equity Type: Owner's Capital, Retained Earnings
    - Revenue Type: Sales Revenue, Service Revenue
    - Expense Type: Cost of Goods Sold, Operating Expenses
    """
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique account code (e.g., 1000, 2000, 3000)"
    )
    name = models.CharField(
        max_length=200,
        help_text="Main account name"
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        help_text="Type of account"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this main account"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this account is currently active"
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Main Account'
        verbose_name_plural = 'Main Accounts'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_normal_balance(self):
        """
        Returns the normal balance side for this account type.
        Assets and Expenses have debit normal balance.
        Liabilities, Equity, and Revenue have credit normal balance.
        """
        if self.account_type in [AccountType.ASSET, AccountType.EXPENSE]:
            return 'DEBIT'
        return 'CREDIT'

    def get_balance(self):
        """
        Calculate the total balance of this main account by summing all sub-accounts.
        Returns a Decimal value.
        """
        total = Decimal('0.00')
        for sub_account in self.sub_accounts.filter(is_active=True):
            total += sub_account.get_balance()
        return total

    def clean(self):
        """Validation before saving"""
        super().clean()
        # Ensure code is uppercase and properly formatted
        if self.code:
            self.code = self.code.strip().upper()


class SubAccount(BaseModel):
    """
    Sub-accounts under Main Accounts for detailed tracking.
    Examples under "Cash" Main Account:
    - Cash on Hand
    - Petty Cash
    - Cash in Bank - Checking Account
    - Cash in Bank - Savings Account

    For Expense accounts, can be categorized under Account Classes like:
    - Cost of Goods Sold
    - Selling Expenses
    - Administrative Expenses
    """
    main_account = models.ForeignKey(
        MainAccount,
        on_delete=models.PROTECT,
        related_name='sub_accounts',
        help_text="Parent main account"
    )
    account_class = models.ForeignKey(
        AccountClass,
        on_delete=models.PROTECT,
        related_name='sub_accounts',
        null=True,
        blank=True,
        help_text="Optional: Account class for additional categorization (e.g., COGS, Selling, Administrative)"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique sub-account code (e.g., 1001, 1002)"
    )
    name = models.CharField(
        max_length=200,
        help_text="Sub-account name"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of this sub-account"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this sub-account is currently active"
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Sub Account'
        verbose_name_plural = 'Sub Accounts'

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def account_type(self):
        """Return the account type from parent main account"""
        return self.main_account.account_type

    def get_normal_balance(self):
        """
        Inherit normal balance from parent main account.
        """
        return self.main_account.get_normal_balance()

    def get_balance(self):
        """
        Calculate the current balance of this sub-account from posted transactions.
        Only includes posted journal entries for accurate reporting.
        """
        # Sum all posted transaction lines for this sub-account
        total_debits = self.transaction_lines.filter(
            journal_entry__is_posted=True
        ).aggregate(
            total=models.Sum('debit', default=Decimal('0'))
        )['total'] or Decimal('0.00')

        total_credits = self.transaction_lines.filter(
            journal_entry__is_posted=True
        ).aggregate(
            total=models.Sum('credit', default=Decimal('0'))
        )['total'] or Decimal('0.00')

        # Calculate balance based on normal balance side
        if self.get_normal_balance() == 'DEBIT':
            # Assets and Expenses: Debit increases, Credit decreases
            return total_debits - total_credits
        else:
            # Liabilities, Equity, Revenue: Credit increases, Debit decreases
            return total_credits - total_debits

    def clean(self):
        """Validation before saving"""
        super().clean()
        # Ensure code is uppercase and properly formatted
        if self.code:
            self.code = self.code.strip().upper()

        # Validate that sub-account code starts with main account code prefix
        if self.main_account and self.code:
            # This is optional validation - can be removed if not needed
            # Ensures organizational structure (e.g., 1000 -> 1001, 1002)
            pass

    def save(self, *args, **kwargs):
        """Override save to run validations"""
        self.clean()
        super().save(*args, **kwargs)
