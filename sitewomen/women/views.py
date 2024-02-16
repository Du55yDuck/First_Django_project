from django.http import HttpResponse, HttpResponseNotFound, Http404  # импорт наших классов из django.http
from django.shortcuts import render, redirect  # импорт redirect

# Наше представление в виде функции, формирующее внешний вид сайта

menu = [{'title': "О сайте", 'url_name': 'about'},  # список со словарей из названия пункта меню и названий маршрутов
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]

data_db = [  # имитация базы данных
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]

cats_db = [  # список категорий id для примера
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'},
]


def index(request):  # request - ссылка на запрос HttpRequest
    data = {  # словарь с данными из шаблона index.html работает с помощью render (для примера)
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,  # через posts идет обращение к data_db
        'cat_selected': 0,  # cat_selected из list_categories == 0, так как выделяются все рубрики для выделения
    }
    return render(request, 'women/index.html', context=data)  # аналог кода выше, но с render
    # (context=data - 3 аргумент с явным параметром) (нужно прописывать путь!)


def about(request):  # ф-я представления about(о сайте) + render ( 3 - аргумент в виде словаря в шаблоне about)
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})  # путь к шаблону
    # about.html !(Джанго начинает поиск сверху)!


def show_post(request, post_id):  # ф-я для организации ссылки post_id
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def addpage(request):  # ф-я для добавления контента
    return HttpResponse("Добавление статьи")


def contact(request):  # ф-я для контактов
    return HttpResponse("Обратная связь")


def login(request):  # ф-я для авторизации
    return HttpResponse("Авторизация")


def show_category(request, cat_id):  # ф-я для вывода категории
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404
