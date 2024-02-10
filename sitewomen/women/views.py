from django.http import HttpResponse, HttpResponseNotFound, Http404  # импорт наших классов из django.http
from django.shortcuts import render, redirect  # импорт redirect
from django.template.loader import render_to_string  # импорт из шаблонизатора Джанго ф-ии render_to_string
from django.urls import reverse  # импорт reverse для примера
from django.template.defaultfilters import slugify  # пример использования фильтров, импортировав из Джанго

# Наше представление в виде функции, формирующее внешний вид сайта

menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']  # список для примера


class MyClass:  # класс для примера
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):  # request - ссылка на запрос HttpRequest
    # t = render_to_string('women/index.html')  # обработка шаблона с помощью ф-ии render_to_string(1 вариант)
    # return HttpResponse(t)  # t - текстовый вариант index.html
    data = {  # словарь с данными из шаблона index.html работает с помощью render (для примера)
        'title': 'Главная страница?',  # знак ? для примера работы фильтра cut
        'menu': menu,
        'float': 28.56,
        'lst': [1, 2, 'abc', True],
        'set': {1, 2, 3, 4, 5},
        'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
        'class_object': MyClass(10, 20),
        'url': slugify("The main page")  # пример фильтра slugify
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

# Варианты redirect: a) return redirect('/') - переход на гл стр с кодом 302 b) return redirect('/', permanent=True)-301
# c) return redirect(index) - переход на главную страницу через ф-ю index
# d) return redirect('home') - переход по имени маршрута, которые прописываются в urls.py
# ! 301 - страница перемещена на др постоянный URL, 302 - временно
# Варианты redirect + reverse: if year > 2023: - для вычисления URL адресов
# uri = reverse('cats', args=('music', )) - маршрут cats + параметры в виде коллекции(list, tuple...)
# return redirect(uri) - возвращает вычисленный URL
# Варианты с классами HttpResponseRedirect такие же return HttpResponseRedirect('/' или 'home' или uri) - 302
# либо return HttpResponsePermanentRedirect() - перенаправление с кодом 301 (требуют вычисленного URL, аналог redirect)


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404
