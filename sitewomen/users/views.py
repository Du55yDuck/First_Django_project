from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm


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


class ProfileUser(LoginRequiredMixin, UpdateView):  # Класс пред-я для профиля пользователя(Mixin - запрет просмотра
    model = get_user_model()          # профиля для не авторизованных пользователей, Update - изменение текущих записей.
    form_class = ProfileUserForm  # ссылка на форму ProfileUserForm
    template_name = 'users/profile.html'  # шаблон
    extra_context = {'title': "Профиль пользователя"}  # заголовок + текс

    def get_success_url(self):  # метод для перенаправления на указанный адрес, после изменения записей
        return reverse_lazy('users:profile')  # возврат на текущую страницу

    def get_object(self, queryset=None):  # Метод, возвращающий запись, которая редактируется
        return self.request.user  # обращение к текущему пользователю
