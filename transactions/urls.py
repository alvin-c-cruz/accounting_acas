from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('new/', views.transaction_new, name='transaction_new'),
    path('<int:entry_id>/', views.transaction_detail, name='transaction_detail'),
    path('<int:entry_id>/edit/', views.transaction_edit, name='transaction_edit'),
    path('<int:entry_id>/post/', views.transaction_post, name='transaction_post'),
    path('<int:entry_id>/unpost/', views.transaction_unpost, name='transaction_unpost'),
]
