from django.urls import path  # импорт фунцкии path из django.urls
from . import views  # импорт views из текущего модуля

urlpatterns = [
    path('', views.index),  # http://127.0.0.1:8000 - маршрут отвечает за главную страницу
    path('cats/', views.categories),  # http://127.0.0.1:8000/cats/ - маршрут за страницу cats
]
