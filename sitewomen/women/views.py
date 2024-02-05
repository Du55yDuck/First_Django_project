from django.http import HttpResponse, HttpResponseNotFound, Http404  # импорт наших классов из django.http
from django.shortcuts import render

# Наше представление в виде функции, формирующее внешний вид сайта


def index(request):  # request - ссылка на запрос HttpRequest
    return HttpResponse("Страница приложения women")  # вернет экземпляр класса с ответом


def categories(request, cat_id):  # вторая ф-я представления + параметр cat_id принимающие целые числа в конце адреса
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")  # возвращает экземпляр с ответом


def categories_by_slug(request, cat_slug):  # 3-я ф-я представления для вывода slug в категориях
    if request.POST:  # условие для POST запроса(если он не пустой, то вывести его в консоль с помощью ф-ии QueryDict
        print(request.POST)  # вывод POST запроса(также можно работать с GET запросами)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")  # возвращает slug и набор символов


def archive(request, year):  # ф-я представления для archive
    if year > 2023:  # условие для обработки исключения для archive
        raise Http404()  # генерация исключения 404 ссылающееся на page_not_found, благодаря handler404
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")  # возвращает ответ ф-строку с годом(4 цифры)


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404
