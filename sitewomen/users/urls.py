from django.urls import path  # импорт функций path
from . import views  # импорт views из текущего модуля

app_name = "users"  # обязательное определение переменной с названием users

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),  # маршрут для авторизации с помощью class LoginUser
    path('logout/', views.logout_user, name='logout'),  # маршрут для выхода с помощью ф-ии logout_user.
]

