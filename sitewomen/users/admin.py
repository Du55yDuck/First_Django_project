from django.contrib import admin  # импорт и подключение модели class User(AbstractUser)
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
