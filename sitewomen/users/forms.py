from datetime import date

from django import forms  # импортируем из django
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):  # класс для авторизации (форма не связана с моделью)
    username = forms.CharField(label="Логин",  # стиль оформления через widget + attrs{класс и стили}
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",  # поле для пароля.
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:  # Класс, указывающий явную связь с моделью + отображаемые поля(класс как дополнение атрибутам выше)
        model = get_user_model()  # get_user_model возвращает текущую модель пользователя(если в будущем модель
        # пользователя меняется, то get_user_model вернет указанную, вместо стандартной - good practice!)
        fields = ['username', 'password']  # поля для отображения


class RegisterUserForm(UserCreationForm):  # Класс форма для рег-ии пользователя(связана с моделью) тип UserCreationForm
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повтор пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # Обязательные атрибуты (поля для заполнения)

    class Meta:  # Вложенный класс (так как основной класс связан с моделью)
        model = get_user_model()  # Возвращает текущую модель пользователя
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']  # поля отображаемые в форме
        labels = {  # метки для полей
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {  # через атрибут widgets назначить стили для указанных полей
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):  # Валидатор проверки на уникальность email-адреса
        email = self.cleaned_data['email']  # данные с ключом по email
        if get_user_model().objects.filter(email=email).exists():  # Из модели пользователя отбирает польз-я по email,
            # если такой найден, тогда отрабатывает генерация исключения
            raise forms.ValidationError("Такой E-mail уже существует!")  # исключение, если проверка не прошла
        return email


class ProfileUserForm(forms.ModelForm):  # Форма для профиля пользователя(отображаемые поля), связан с моделью
    username = forms.CharField(disabled=True, label="Логин", widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label="E-mail", widget=forms.TextInput(attrs={'class': 'form-input'}))
    this_year = date.today().year  # Стандартный модуль для получения текущего года
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))  # Спец
    #  widget для удобного заполнения поля даты + диапазон возраста от 5-100 лет

    class Meta:
        model = get_user_model()  # Стараться использовать get_user_model() вместо обычного обращения user!
        fields = ['photo', 'username', 'email', 'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {  # стили полей
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):  # Форма для смены пароля(наследие от стандартного PasswordChangeForm)
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",  # + {'class': 'form-input'} - стиль полей
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
