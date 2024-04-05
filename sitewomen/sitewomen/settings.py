"""
Django settings for sitewomen project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n4ea1n#g0ksne#xhk$5yovwm8k5)c7id_5kpm(n-rsumk39m1a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Режим отладки, True - вывод стандартной инф-ии из Джанго(False дает возможность выводить свои варианты
# содержимое функций представления для клиента(errors - 400, 403, 404, 500)

ALLOWED_HOSTS = ['127.0.0.1']  # указать наш хост для разрешения ввода изменений
INTERNAL_IPS = ["127.0.0.1"]  # адрес для django toolbar

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',  # доп пакет для удобства отображения sql запросов
    'women.apps.WomenConfig',  # должно быть указано наше приложение!
    'users',  # приложение users для авторизации пользователей + оригинальное имя
    "debug_toolbar",  # приложение django toolbar
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # SessionMiddleware - требуются для корректной работы users
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # AuthenticationMiddleware- аналогично SessionMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # установка django toolbar
]

ROOT_URLCONF = 'sitewomen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [  # позволяет прописывать не стандартные пути к шаблонам(такие, как templates)
            BASE_DIR / 'templates',  # путь к нашей не стандартной директории
        ],
        'APP_DIRS': True,  # ищет шаблоны в директориях внутри созданных приложений(используя пути к файлам)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # обеспечивает работу переменной request в шаблонах
                'django.contrib.auth.context_processors.auth',  # обеспечивает переменной user в шаблонах
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_women_context',  # пользовательский конт проц из шаблона get_women_context
            ],
        },
    },
]

WSGI_APPLICATION = 'sitewomen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'  # русский язык админки 'en-US'- по умолчанию

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'  # префикс к URL-адресам
STATICFILES_DIRS = [
    BASE_DIR / 'static', ]  # указать не стандартные маршруты для static-каталогов/файлов

MEDIA_ROOT = BASE_DIR / 'media'  # общий каталог для загруженных файлов
MEDIA_URL = '/media/'  # авто добавления префикса media ко всем загружаемым медиа-файлам для добавления и связи маршрута
# с каталогом медеи-файлов общего проекта.

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'  # Атрибут для перехода по указанному маршруту(главная страница), после успешной авторизации
# Аналог спец метода def get_success_url() - имеет больший приоритет.
LOGOUT_REDIRECT_URL = 'home'  # Перенаправление по указанному маршруту(главная страница), после выхода из системы.
LOGIN_URL = 'users:login'  # перенаправление на указанный адрес не авторизованного пользователя(пространство имен users)
