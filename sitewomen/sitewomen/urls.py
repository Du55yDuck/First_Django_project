"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # импорт include

from women import views  # импорт наших представлений(функций index, categories) из директории women - views.py
from women.views import page_not_found  # импорт page_not_found(после его представления!)

# + папку sitewomen сделали sourse root(рабочий каталог) из-за конфликта в import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),  # Спец. Функция include позволяет подключить все маршруты автоматически. Если
    # на месте '' прописать свой индекс и еще в файле women/urls.py - то он будет добавляться к адресу автоматически

    # Вариант ниже менее оптимизированный, но также возможен
    # path('cats/', views.categories),  # http://127.0.0.1:8000/cats/ - адрес + добавление индекса cats с каталогом
    # статей по рубрикам
    # path('', views.index) - вариант вручную с указанием маршрута на http://127.0.0.1:8000 где '' указывает на
    # отсутствие индекса после 8000. Нарушает принцип независимости приложений сайта, но допустим!

]

handler404 = page_not_found  # обработчик handler404 + ссылка на нашу ф-ию для вывода нашего сообщения при ошибке
