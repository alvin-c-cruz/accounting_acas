from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index, name='reports_index'),
    path('balance-sheet/', views.balance_sheet, name='balance_sheet'),
    path('income-statement/', views.income_statement, name='income_statement'),
    path('trial-balance/', views.trial_balance, name='trial_balance'),
    path('cash-flow/', views.cash_flow, name='cash_flow'),
]
