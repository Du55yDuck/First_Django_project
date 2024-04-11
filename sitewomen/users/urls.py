from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path  # импорт функций path
from . import views  # импорт views из текущего модуля

app_name = "users"  # обязательное определение переменной с названием users

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),  # маршрут для авторизации с помощью class LoginUser
    path('logout/', views.logout_user, name='logout'),  # маршрут для выхода с помощью ф-ии logout_user.

    path('password-change/', views.UserPasswordChange.as_view(), name="password_change"),  # Пользовательский класс для
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
         name="password_change_done"),  # смены пароля (template_name=переопределение шаблона со станд-го на пользов-ий)

    path('register/', views.RegisterUser.as_view(), name='register'),  # маршрут для класса регистрации пользователя
    path('profile/', views.ProfileUser.as_view(), name='profile'),  # маршрут для класса профиля пользователя
]
