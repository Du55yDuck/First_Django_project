from django.http import HttpResponse
from django.shortcuts import render

# Наше представление в виде функции, формирующее внешний вид сайта


def index(request):  # request - ссылка на запрос HttpRequest
    return HttpResponse("Страница приложения women")  # вернет экземпляр класса с ответом


def categories(request, cat_id):  # вторая ф-я представления + параметр cat_id принимающие целые числа в конце адреса
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")  # возвращает экземпляр с ответом


def categories_by_slug(request, cat_slug):  # 3-я ф-я представления для вывода slug в категориях
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")  # возвращает slug и набор символов


def archive(request, year):  # ф-я представления для archive
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")  # возвращает ответ ф-строку с годом(4 цифры)
