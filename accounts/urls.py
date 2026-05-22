from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.chart_of_accounts, name='chart_of_accounts'),
    path('<int:account_id>/', views.account_detail, name='account_detail'),
]
