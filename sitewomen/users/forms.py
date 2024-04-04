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

