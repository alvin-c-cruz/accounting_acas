// Dashboard JavaScript

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Accounting System Dashboard Loaded');

    // Load dashboard data
    loadDashboardData();

    // Set up auto-refresh every 60 seconds
    setInterval(loadDashboardData, 60000);
});

// Load dashboard data from API
async function loadDashboardData() {
    try {
        // Fetch summary data
        const summaryResponse = await fetch('/api/dashboard/summary');
        if (summaryResponse.ok) {
            const summaryData = await summaryResponse.json();
            updateSummaryCards(summaryData);
        }

        // Fetch recent transactions
        const transactionsResponse = await fetch('/api/transactions/recent?limit=10');
        if (transactionsResponse.ok) {
            const transactions = await transactionsResponse.json();
            updateTransactionsTable(transactions);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Update summary cards with data
function updateSummaryCards(data) {
    const cards = document.querySelectorAll('.card .amount');

    if (data.total_assets !== undefined) {
        cards[0].textContent = formatCurrency(data.total_assets);
    }

    if (data.total_liabilities !== undefined) {
        cards[1].textContent = formatCurrency(data.total_liabilities);
    }

    if (data.equity !== undefined) {
        cards[2].textContent = formatCurrency(data.equity);
    }

    if (data.monthly_revenue !== undefined) {
        cards[3].textContent = formatCurrency(data.monthly_revenue);
    }
}

// Update transactions table
function updateTransactionsTable(transactions) {
    const tbody = document.querySelector('.transactions-table tbody');

    if (!transactions || transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No transactions yet. Create your first transaction to get started.</td></tr>';
        return;
    }

    tbody.innerHTML = transactions.map(transaction => `
        <tr>
            <td>${formatDate(transaction.date)}</td>
            <td>${escapeHtml(transaction.description)}</td>
            <td>${escapeHtml(transaction.account)}</td>
            <td>${transaction.debit ? formatCurrency(transaction.debit) : '-'}</td>
            <td>${transaction.credit ? formatCurrency(transaction.credit) : '-'}</td>
            <td>${formatCurrency(transaction.balance)}</td>
        </tr>
    `).join('');
}

// Format currency with proper decimal places
function formatCurrency(amount) {
    if (amount === null || amount === undefined) {
        return '$0.00';
    }

    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

// Format date to readable format
function formatDate(dateString) {
    if (!dateString) return '-';

    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(date);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Handle network errors gracefully
window.addEventListener('online', function() {
    console.log('Connection restored');
    loadDashboardData();
});

window.addEventListener('offline', function() {
    console.log('Connection lost');
});
