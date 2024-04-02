from django import forms  # импортируем из django


class LoginUserForm(forms.Form):  # класс для авторизации (форма не связана с моделью)
    username = forms.CharField(label="Логин",  # стиль оформления через widget + attrs{класс и стили}
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",  # поле для пароля.
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))
