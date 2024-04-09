from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from users.forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):  # класс типа LoginView для авторизации(наследуется от LoginView)
    form_class = LoginUserForm  # атрибут формы класса(наследуется от стандартной AuthenticationForm)
    template_name = 'users/login.html'  # название и путь к шаблону
    extra_context = {'title': 'Авторизация'}  # передача в шаблон заголовка

    # def get_success_url(self):  # спец метод переопределяющий переход на указанную стран-у, после успешной авторизации
    #     return reverse_lazy('home')  # явно указать возврат и маршрут страницы(в данном случае - главная)


def logout_user(request):  # ф-я для выхода авторизованного пользователя
    logout(request)  # спец ф-я logout для выхода из системы
    return HttpResponseRedirect(reverse("home"))  # перенаправление по указанному маршруту(главная страница)


class RegisterUser(CreateView):  # Класс аналог def register. Проверяет корректность заполненности формы и сохр-ет в БД.
    form_class = RegisterUserForm  # атрибут используемой формы
    template_name = 'users/register.html'  # используемый шаблон
    extra_context = {'title': "Регистрация"}  # Заголовок с текстом
    success_url = reverse_lazy('users:login')  # маршрут для перенаправления пользователя после успешной регистрации.


# def register(request):  # ф-я для регистрации
#     if request.method == 'POST':  # Если метод передачи POST
#         form = RegisterUserForm(request.POST)  # Создать заполненную форму с указанными данными
#         if form.is_valid():  # проверка на корректность заполненности всех полей
#             user = form.save(commit=False)  # не сохранять в БД
#             user.set_password(form.cleaned_data['password'])  # спец метод set_password шифрует пароль и заносит его в
#             user.save()  # атрибут RegisterUserForm -> password. Далее сохранение в БД
#             return render(request, 'users/register_done.html')  # указать шаблон
#     else:  # Иначе сформировать пустую форму
#         form = RegisterUserForm()  # объект формы RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})  # вывеси форму в шаблон
