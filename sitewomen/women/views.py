from django.http import HttpResponse, HttpResponseNotFound, Http404  # импорт наших классов из django.http
from django.shortcuts import render, redirect  # импорт redirect

# Наше представление в виде функции, формирующее внешний вид сайта

menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']  # список для примера

data_db = [  # имитация базы данных
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


def index(request):  # request - ссылка на запрос HttpRequest
    data = {  # словарь с данными из шаблона index.html работает с помощью render (для примера)
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,  # через posts идет обращение к data_db
    }
    return render(request, 'women/index.html', context=data)  # аналог кода выше, но с render
    # (context=data - 3 аргумент с явным параметром) (нужно прописывать путь!)


def about(request):  # ф-я представления about(о сайте) + render ( 3 - аргумент в виде словаря в шаблоне about)
    return render(request, 'women/about.html', {'title': 'О сайте'})  # путь к шаблону about.html
    # (Джанго начинает поиск сверху)


def categories(request, cat_id):  # вторая ф-я представления + параметр cat_id принимающие целые числа в конце адреса
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")  # возвращает экземпляр с ответом


def categories_by_slug(request, cat_slug):  # 3-я ф-я представления для вывода slug в категориях
    if request.POST:  # условие для POST запроса(если он не пустой, то вывести его в консоль с помощью ф-ии QueryDict
        print(request.POST)  # вывод POST запроса(также можно работать с GET запросами)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")  # возвращает slug и набор символов


def archive(request, year):  # ф-я представления для archive
    if year > 2023:  # условие для обработки исключения для archive
        return redirect('cats', 'music')  # перенапр-е с archive на slug:cat_slug с кодом 302 + маршрут music
        # raise Http404()  # генерация исключения 404 ссылающееся на page_not_found, благодаря handler404
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")  # возвращает ответ ф-строку с годом(4 цифры)


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404
