from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy  # импорт функций path
from . import views  # импорт views из текущего модуля

app_name = "users"  # обязательное определение переменной с названием users

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),  # маршрут для авторизации с помощью class LoginUser
    path('logout/', views.logout_user, name='logout'),  # маршрут для выхода с помощью ф-ии logout_user.

    path('password-change/', views.UserPasswordChange.as_view(), name="password_change"),  # Пользовательский класс для
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
         name="password_change_done"),  # смены пароля (template_name=переопределение шаблона со станд-го на пользов-ий)

    path('password-reset/',  # маршруты для стандартных классов сброса пароля
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",  # пользовательский шаблон
             email_template_name="users/password_reset_email.html",  # шаблон, формирующий текст сообщения на email
             success_url=reverse_lazy("users:password_reset_done")), name='password_reset'),  # перенаправление
    path('password-reset/done/',  # сообщение о сбросе пароля
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/',  # маршруты для стан-ых классов восстановления пароля
         PasswordResetConfirmView.as_view(  # спец токен (из доку) --> на почту для восстановления пароля
             template_name="users/password_reset_confirm.html",  # пользовательский шаблон
             success_url=reverse_lazy("users:password_reset_complete")),  name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),  # сообщение об успешности восстановления и ссылка на вход



    path('register/', views.RegisterUser.as_view(), name='register'),  # маршрут для класса регистрации пользователя
    path('profile/', views.ProfileUser.as_view(), name='profile'),  # маршрут для класса профиля пользователя
]
