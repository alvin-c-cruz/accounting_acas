from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('pending-approval/', views.pending_approval_view, name='pending_approval'),
]
