from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('export/', views.export_users_pdf, name='export_users_pdf'),
    path('export_success/', views.export_success, name='export_success'),
]
