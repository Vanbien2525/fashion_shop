from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='base'),
    path('contact/', views.contact, name='contact'),
]
