from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend  # импорт BaseBackend


class EmailAuthBackend(BaseBackend):  # Класс от BaseBackend для авторизации(методы copy from backends.py)
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()  # ссылка на модель user
        try:  # получить текущего пользователя по модели
            user = user_model.objects.get(email=username)  # использовать username(login) как email
            if user.check_password(password):  # стандартный метод проверки паролей для модели user
                return user  # если проверка прошла, то вернуть объект user
            return None  # иначе - None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):  # Два исключения: если запись не была
            # найдена, если найдены несколько записей по одному email-у.
            return None  # возвращает None после исключения.

    def get_user(self, user_id):  # Метод для получения модели user по user_id или возвращать None
        user_model = get_user_model()  # получить текущую модель
        try:  # получить объект пользователя
            return user_model.objects.get(pk=user_id)  # Вернуть текущего пользователя по pk
        except user_model.DoesNotExist:  # Исключение, если пользователь не найден
            return None
