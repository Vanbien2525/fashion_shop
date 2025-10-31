from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.base, name='base'),      # trang mặc định
    path('index/', views.index, name='index'),  # trang index sau khi login
]
