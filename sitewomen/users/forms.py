from django import forms  # импортируем из django
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):  # класс для авторизации (форма не связана с моделью)
    username = forms.CharField(label="Логин",  # стиль оформления через widget + attrs{класс и стили}
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",  # поле для пароля.
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:  # Класс, указывающий явную связь с моделью + отображаемые поля(класс как дополнение атрибутам выше)
        model = get_user_model()  # get_user_model возвращает текущую модель пользователя(если в будущем модель
        # пользователя меняется, то get_user_model вернет указанную, вместо стандартной - good practice!)
        fields = ['username', 'password']  # поля для отображения


class RegisterUserForm(forms.ModelForm):  # Класс форма для регистрации пользователя(связана с моделью)
    username = forms.CharField(label="Логин")  # Атрибуты (поля для заполнения) - обязательное поле
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())  # также обязательное поле
    password2 = forms.CharField(label="Повтор пароль", widget=forms.PasswordInput())  # Поле для подтверждения пароля

    class Meta:  # Вложенный класс (так как основной класс связан с моделью)
        model = get_user_model()  # Возвращает текущую модель пользователя
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']  # поля отображаемые в форме
        labels = {  # метки для полей
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        def clean_password2(self):  # Валидатор для проверки пароля на равенство
            cd = self.cleaned_data  # словарь(очищенные данные)
            if cd['password'] != cd['password2']:  # Проверка на равенство паролей
                raise forms.ValidationError("Пароли не совпадают!")  # исключение, если пароли не совпадают
            return cd['password']

        def clean_email(self):  # Валидатор проверки на уникальность email-адреса
            email = self.cleaned_data['email']  # данные с ключом по email
            if get_user_model().objects.filter(email=email).exists():  # Из модели пользователя отобр польз-я по email,
                # если такой найден, тогда отрабатывает генерация исключения
                raise forms.ValidationError("Такой E-mail уже существует!")  # исключение, если проверка не прошла
            return email
