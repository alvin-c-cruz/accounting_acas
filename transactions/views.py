from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import JournalEntry, TransactionLine
from .forms import JournalEntryForm, TransactionLineFormSet


@login_required
def transaction_list(request):
    """Display list of all journal entries"""
    entries = JournalEntry.objects.all().prefetch_related('lines').order_by('-date', '-entry_number')

    context = {
        'entries': entries,
        'total_entries': entries.count(),
        'posted_entries': entries.filter(is_posted=True).count(),
        'draft_entries': entries.filter(is_posted=False).count(),
    }

    return render(request, 'transactions/transaction_list.html', context)


@login_required
def transaction_new(request):
    """Create a new journal entry with transaction lines"""
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        formset = TransactionLineFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the journal entry
                    journal_entry = form.save(commit=False)
                    journal_entry.created_by = request.user
                    journal_entry.updated_by = request.user
                    journal_entry.save()

                    # Save the transaction lines
                    formset.instance = journal_entry
                    lines = formset.save(commit=False)

                    for line in lines:
                        line.created_by = request.user
                        line.updated_by = request.user
                        line.save()

                    # Delete any marked for deletion
                    for line in formset.deleted_objects:
                        line.delete()

                    # Check if balanced
                    if journal_entry.is_balanced():
                        messages.success(
                            request,
                            f'Journal entry {journal_entry.entry_number} created successfully! '
                            f'Entry is balanced: ${journal_entry.get_total_debits()}'
                        )
                    else:
                        messages.warning(
                            request,
                            f'Journal entry {journal_entry.entry_number} created but is UNBALANCED. '
                            f'Debits: ${journal_entry.get_total_debits()}, '
                            f'Credits: ${journal_entry.get_total_credits()}'
                        )

                    return redirect('transactions:transaction_detail', entry_id=journal_entry.id)

            except Exception as e:
                messages.error(request, f'Error creating journal entry: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JournalEntryForm()
        formset = TransactionLineFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': 'New Journal Entry',
        'action': 'Create',
    }

    return render(request, 'transactions/transaction_form.html', context)


@login_required
def transaction_detail(request, entry_id):
    """Display details of a specific journal entry"""
    entry = get_object_or_404(JournalEntry, id=entry_id)
    lines = entry.lines.all().select_related('sub_account__main_account')

    context = {
        'entry': entry,
        'lines': lines,
    }

    return render(request, 'transactions/transaction_detail.html', context)


@login_required
def transaction_edit(request, entry_id):
    """Edit an existing journal entry"""
    entry = get_object_or_404(JournalEntry, id=entry_id)

    # Don't allow editing of posted entries
    if entry.is_posted:
        messages.error(request, 'Cannot edit a posted journal entry. Please unpost it first.')
        return redirect('transactions:transaction_detail', entry_id=entry.id)

    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        formset = TransactionLineFormSet(request.POST, instance=entry)

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Save the journal entry
                    journal_entry = form.save(commit=False)
                    journal_entry.updated_by = request.user
                    journal_entry.save()

                    # Save the transaction lines
                    lines = formset.save(commit=False)

                    for line in lines:
                        if not line.pk:
                            line.created_by = request.user
                        line.updated_by = request.user
                        line.save()

                    # Delete any marked for deletion
                    for line in formset.deleted_objects:
                        line.delete()

                    # Check if balanced
                    if journal_entry.is_balanced():
                        messages.success(
                            request,
                            f'Journal entry {journal_entry.entry_number} updated successfully!'
                        )
                    else:
                        messages.warning(
                            request,
                            f'Journal entry is UNBALANCED. '
                            f'Debits: ${journal_entry.get_total_debits()}, '
                            f'Credits: ${journal_entry.get_total_credits()}'
                        )

                    return redirect('transactions:transaction_detail', entry_id=journal_entry.id)

            except Exception as e:
                messages.error(request, f'Error updating journal entry: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JournalEntryForm(instance=entry)
        formset = TransactionLineFormSet(instance=entry)

    context = {
        'form': form,
        'formset': formset,
        'entry': entry,
        'title': f'Edit Journal Entry {entry.entry_number}',
        'action': 'Update',
    }

    return render(request, 'transactions/transaction_form.html', context)


@login_required
def transaction_post(request, entry_id):
    """Post a journal entry"""
    entry = get_object_or_404(JournalEntry, id=entry_id)

    try:
        entry.post(user=request.user)
        messages.success(request, f'Journal entry {entry.entry_number} posted successfully!')
    except Exception as e:
        messages.error(request, f'Error posting entry: {str(e)}')

    return redirect('transactions:transaction_detail', entry_id=entry.id)


@login_required
def transaction_unpost(request, entry_id):
    """Unpost a journal entry"""
    entry = get_object_or_404(JournalEntry, id=entry_id)

    try:
        entry.unpost(user=request.user)
        messages.success(request, f'Journal entry {entry.entry_number} unposted successfully!')
    except Exception as e:
        messages.error(request, f'Error unposting entry: {str(e)}')

    return redirect('transactions:transaction_detail', entry_id=entry.id)
