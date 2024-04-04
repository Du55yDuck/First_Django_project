from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from users.forms import LoginUserForm


class LoginUser(LoginView):  # класс типа LoginView для авторизации(наследуется от LoginView)
    form_class = LoginUserForm  # атрибут формы класса(наследуется от стандартной AuthenticationForm)
    template_name = 'users/login.html'  # название и путь к шаблону
    extra_context = {'title': 'Авторизация'}  # передача в шаблон заголовка

    # def get_success_url(self):  # спец метод переопределяющий переход на указанную стран-у, после успешной авторизации
    #     return reverse_lazy('home')  # явно указать возврат и маршрут страницы(в данном случае - главная)


# def login_user(request):  # ф-я для авторизации
#     if request.method == 'POST':  # Если метод передачи данных == POST
#         form = LoginUserForm(request.POST)  # Сформировать объект формы с заполненными данными
#         if form.is_valid():  # is_valid проверяет на корректность заполнения полей
#             cd = form.cleaned_data  # У объекта form появляется коллекция clean_data
#             user = authenticate(request, username=cd['username'],  # Спец ф-я authenticate из Джанго для проверки
#                                 password=cd['password'])  # валидности имени пользователя и пароля из БД.
#             if user and user.is_active:  # Если user был найден в БД и активен (аутентификация прошла успешно)
#                 login(request, user)  # авторизация пользователя с помощью спец ф-ии login из Джанго.
#                 return HttpResponseRedirect(reverse('home'))  # если прошло успешно, то переход на главную страницу
#     else:
#         form = LoginUserForm()  # Иначе сформировать объект формы(пустой) и передать в шаблон
#
#     return render(request, 'users/login.html', {'form': form})  # Ответ для пользователя через
# render, шаблон login.html + словарь с передачей form


def logout_user(request):  # ф-я для выхода авторизованного пользователя
    logout(request)  # спец ф-я logout для выхода из системы
    return HttpResponseRedirect(reverse("home"))  # перенаправление по указанному маршруту(главная страница)
