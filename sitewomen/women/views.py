from django.http import HttpResponse
from django.shortcuts import render

# Наше представление в виде функции, формирующее внешний вид сайта


def index(request):  # request - ссылка на запрос HttpRequest
    return HttpResponse("Страница приложения women")  # вернет экземпляр класса с ответом


def categories(request):  # вторая ф-я представления
    return HttpResponse("<h1>Статьи по категориям</h1>")  # возвращает экземпляр с ответом
