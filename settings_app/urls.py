from django.urls import path
from . import views

app_name = 'settings_app'

urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
