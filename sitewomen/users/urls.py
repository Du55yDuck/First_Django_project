from django.urls import path  # импорт функций path
from . import views  # импорт views из текущего модуля

app_name = "users"  # обязательное определение переменной с названием users

urlpatterns = [
    path('login/', views.login_user, name='login'),  # маршрут для авторизации с помощью ф-и login_user
    path('logout/', views.logout_user, name='logout'),  # маршрут для выхода с помощью ф-и logout_user
]

