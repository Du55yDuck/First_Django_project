from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginUserForm


def login_user(request):  # ф-я для авторизации
    if request.method == 'POST':  # Если метод передачи данных == POST
        form = LoginUserForm(request.POST)  # Сформировать объект формы с заполненными данными
        if form.is_valid():  # is_valid проверяет на корректность заполнения полей
            cd = form.cleaned_data  # У объекта form появляется коллекция clean_data
            user = authenticate(request, username=cd['username'],  # Спец ф-я authenticate из Джанго для проверки
                                password=cd['password'])  # валидности имени пользователя и пароля из БД.
            if user and user.is_active:  # Если user был найден в БД и активен (аутентификация прошла успешно)
                login(request, user)  # авторизация пользователя с помощью спец ф-ии login из Джанго.
                return HttpResponseRedirect(reverse('home'))  # если прошло успешно, то переход на главную страницу
    else:
        form = LoginUserForm()  # Иначе сформировать объект формы(пустой) и передать в шаблон

    return render(request, 'users/login.html', {'form': form})  # Ответ для пользователя через
# render, шаблон login.html + словарь с передачей form


def logout_user(request):  # ф-я для выхода авторизованного пользователя
    logout(request)  # спец ф-я logout для выхода из сессии
    return HttpResponseRedirect(reverse("users:login"))  # перенаправление на страницу авторизации + reverse(
    # users:login - пространство имен из sitewomen/urls.py) для использования одного имени login в нескольких местах.
