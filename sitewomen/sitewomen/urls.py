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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # импорт include

from sitewomen import settings
from women.views import page_not_found  # импорт page_not_found(после его представления!)
# + папку sitewomen сделали sourse root(рабочий каталог) из-за конфликта в import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),  # Спец. Функция include позволяет подключить все маршруты автоматически. Если
    # на месте '' прописать свой индекс и еще в файле women/urls.py - то он будет добавляться к адресу автоматически
    path('users/', include('users.urls', namespace="users")),  # путь + связка с приложением users + namespace
    path("__debug__/", include("debug_toolbar.urls")),  # путь для django toolbar
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Связка маршрута MEDIA_URL с
    # общим каталогом sitewomen/media (MEDIA_ROOT) в режиме Debug для корректной работы сервера при обращении в этом
    # режиме и в режиме работы.

handler404 = page_not_found  # обработчик handler404 + ссылка на нашу ф-ию для вывода нашего сообщения при ошибке

admin.site.site_header = "Панель администрирования"  # наш заголовок админки
admin.site.index_title = "Известные женщины мира"  # заголовок ниже уровнем
