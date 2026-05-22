from django import forms
from django.forms import inlineformset_factory
from decimal import Decimal
from .models import JournalEntry, TransactionLine
from accounts.models import SubAccount


class JournalEntryForm(forms.ModelForm):
    """Form for creating/editing journal entries"""

    class Meta:
        model = JournalEntry
        fields = ['entry_number', 'date', 'description', 'reference']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'entry_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TransactionLineForm(forms.ModelForm):
    """Form for transaction lines"""

    class Meta:
        model = TransactionLine
        fields = ['sub_account', 'description', 'debit', 'credit']
        widgets = {
            'sub_account': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'debit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'credit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        debit = cleaned_data.get('debit') or Decimal('0')
        credit = cleaned_data.get('credit') or Decimal('0')

        if debit > 0 and credit > 0:
            raise forms.ValidationError("A line cannot have both debit and credit amounts.")

        if debit == 0 and credit == 0:
            raise forms.ValidationError("A line must have either a debit or credit amount.")

        return cleaned_data


# Formset for transaction lines
TransactionLineFormSet = inlineformset_factory(
    JournalEntry,
    TransactionLine,
    form=TransactionLineForm,
    extra=4,  # Show 4 empty forms by default
    can_delete=True,
    min_num=2,  # Require at least 2 lines
    validate_min=True,
)
