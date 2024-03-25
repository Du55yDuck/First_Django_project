from django.http import HttpResponse, HttpResponseNotFound, Http404  # импорт наших классов из django.http
from django.shortcuts import render, redirect, get_object_or_404  # импорт redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles

# Наше представление в виде функции, формирующее внешний вид сайта

menu = [{'title': "О сайте", 'url_name': 'about'},  # список со словарей из названия пункта меню и названий маршрутов
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]


# def index(request):  # request - ссылка на запрос HttpRequest
#     posts = Women.published.all().select_related('cat')  # posts - реализация обращения к БД + filter для
#     # published (все публикации) + оптимизация через select_related(жадная загрузка по внешнему ключу типа ForeignKey
#
#     data = {  # словарь с данными из шаблона index.html работает с помощью render (для примера)
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,  # непосредственно читает данные из БД
#         'cat_selected': 0,  # cat_selected из list_categories == 0, так как выделяются все рубрики для выделения
#     }
#     return render(request, 'women/index.html', context=data)  # аналог кода выше, но с render
#     # (context=data - 3 аргумент с явным параметром) (нужно прописывать путь!)


class WomenHome(ListView):  # Пример класса ListView для отображения произвольных списков (аналог ф-ии def index)
    # model = Women  # модель явно указать для listView
    template_name = 'women/index.html'  # путь к шаблону, который используется
    context_object_name = 'posts'  # атрибут для использования списка статей из модели Women(posts в шаблоне index.html)
    extra_context = {  # позволяет передавать доп данные в шаблон(в данном - добавляет базовые поля на главную страницу)
        'title': 'Главная страница',  # Данные в словарь можно прописать только те, которые известны на момент
        'menu': menu,                 # определения самого класса (Только статические данные - на момент существ класса)
        'cat_selected': 0,
    }

    def get_queryset(self):  # спец метод для отображения только опубликованных статей, если отображаются все статьи.
        return Women.published.all().select_related('cat')  # отображение всех опубликованных статей

    # def get_context_data - метод работал с классом типа TemplateView
    # def get_context_data(self, **kwargs):  # метод для получения динамических данных (данные в момент запроса)
    #     context = super().get_context_data(**kwargs)  # вызов метода get_context_data из базового класса + параметры
    #     context['title'] = 'Главная страница'  # Далее прописываем нужные нам ключи
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))  # Получение cat_selected (выбор категории по
    #     # cat_id через обращение к объекту request в коллекции GET через шаблон
    #     return context


# def handle_uploaded_file(f):  # Спец метод для ручной загрузки файлов по частям с помощью объекта f
#     with open(f"uploads/{f.name}", "wb+") as destination:  # открыть f и прописать маршрут места хранения файла + имя
#         for chunk in f.chunks():
#             destination.write(chunk)  # запись фрагментов файла до полной загрузки через цикл


def about(request):  # ф-я представления about(о сайте) + render ( 3 - аргумент в виде словаря в шаблоне about)
    if request.method == 'POST':  # Если метод загрузки == POST, то def handle... запускается и далее...
        form = UploadFileForm(request.POST, request.FILES)  # форма с данными(коллекции: POST + FILES(работа с файлами))
        if form.is_valid():  # проверка на валидность заполнения формы (загрузка на сервер)
            fp = UploadFiles(file=form.cleaned_data['file'])  # создание новой записи с помощью модели (создаем новый
            fp.save()  # объект этой модели + сохраняем его.
    else:
        form = UploadFileForm()  # Пустая форма для загрузки файла
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})  # путь к шаблону + передача формы в шаблоны
    # about.html !(Джанго начинает поиск сверху)!


# def show_post(request, post_slug):  # ф-я для организации ссылки post_slug
#     post = get_object_or_404(Women, slug=post_slug)  # выводит одну страницу по slug или 404 + импорт Women
#
#     data = {  # передает заголовок статьи, меню, страницу
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'women/post.html', data)  # возвращает шаблон post.html и словарь data

class ShowPost(DetailView):  # класс-аналог def show_post(отображает выбранный пост)
    # model = Women  # модель из которой берется текущая статья
    template_name = 'women/post.html'  # используемый шаблон
    slug_url_kwarg = 'post_slug'  # явно указана переменная, по которой вызывается статья(указать в urls.py - маршрутах)
    context_object_name = 'post'  # переменная из шаблона post.html

    def get_context_data(self, **kwargs):  # метод для вывода актуального заголовка в шапке выбранного поста
        context = super().get_context_data(**kwargs)  # вызов метода из базового класса
        context['title'] = context['post'].title  # Заголовок из переменной context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):  # отобразить статьи только из опубликованных записей, иначе исключение 404
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])  # Women.published - менеджер
    # записей(только публикованные), по slug-у через переменную slug_url_kwargs из ShowPost

# def addpage(request):  # ф-я для добавления контента (возвращает шаблон addpage) + request.GET/POST - показывает инфо
#     if request.method == 'POST':  # Проверка на POST запрос
#         form = AddPostForm(request.POST, request.FILES)  # экземпляр класса нашей формы для отображения в шаблоне
#         if form.is_valid():  # addpage.html + данные. Если проверка на уровне сервера проходит с помощью .is_valid
#             # print(form.cleaned_data)  # выводит очищенные данные в консоль
#             # try: сохранение данных в БД и вывод исключения в случае ошибки
#             #     Women.objects.create(**form.cleaned_data) # Из модели Women.objects создать new объект + распаковать
#             #     return redirect('home')  # если статья добавлена успешно, то переход на главную страницу.
#             # except: # словарь из clean_data(содержит набор всех необходимых полей)
#             #      form.add_error(None, "Ошибка добавления поста") # вывод сообщения об ошибке
#             form.save()  # метод аналог кода выше - сохраняет данные в ДБ women_women
#             return redirect('home')  # перенаправление после записи на главную страницу
#     else:
#         form = AddPostForm()  # Иначе form с GET запросом возвращает form с пустыми полями(GET - уровень браузера)
#
#     data = {  # вспомогательный словарь с данными
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form  # содержит либо form с данными(если POST-запрос), либо с пустыми полями(если GET-запрос)
#     }
#     return render(request, 'women/addpage.html', data)  # передача словаря


class AddPage(View):  # Пример класса представления View. Имеет методы GET/POST... Замена ф-ии выше.
    def get(self, request):  # метод get с обязательным параметром request
        form = AddPostForm()  # создать пустую форму
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'women/addpage.html', data)

    def post(self, request):  # метод post
        form = AddPostForm(request.POST, request.FILES)  # См комментарии в def addpage
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'women/addpage.html', data)


def contact(request):  # ф-я для контактов
    return HttpResponse("Обратная связь")


def login(request):  # ф-я для авторизации
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):  # ф-я для вывода категории (2 независимых sql запроса для разгрузки БД)
    category = get_object_or_404(Category, slug=cat_slug)  # указать модель и критерий поиска slug
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")  # отобрать статьи по категориям через pk
    # + select_related

    data = {
        'title': f'Рубрика: {category.name}',  # отображать название категории.
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=data)


class WomenCategory(ListView):  # Класс-аналог ф-и show_category (отображает список статей)
    template_name = 'women/index.html'  # шаблон для использования
    context_object_name = 'posts'  # использовать posts из шаблона index.html
    allow_empty = False  # атрибут действия при пустом списке(если указать не существующий slug - то вывод 404)

    def get_queryset(self):  # метод для отображения опубликованных статей
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # фильтр для отображения
    # статей по конкретному slug-у(kwargs передает переменную из urlpatterns[category/...] -> cat_slug)

    def get_context_data(self, **kwargs):  # метод для получения динамических данных (данные в момент запроса)
        context = super().get_context_data(**kwargs)  # вызов метода get_context_data из базового класса + параметры
        cat = context['posts'][0].cat  # posts передается из ListView(Для вывода категории по [0] индексу записи)
        context['title'] = 'Категория - ' + cat.name  # Далее прописываем нужные нам ключи
        context['menu'] = menu
        context['cat_selected'] = cat.pk  # Получение cat_selected (выбор категории по id)
        return context


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404


class TagPostList(ListView):  # класс-аналог def show_tag_postlist(отображает статью по выбранному тегу)
    template_name = 'women/index.html'  # путь к шаблону
    context_object_name = 'posts'  # использовать переменную posts из шаблона
    allow_empty = False  # 404 при не верном slug

    def get_context_data(self, *, object_list=None, **kwargs):  # метод для получения динамических данных
        context = super().get_context_data(**kwargs)  # вызов метода get_context_data из базового класса + параметры
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag  # Далее прописываем нужные нам ключи
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):  # выбор статей по указанным тегам
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

# def show_tag_postlist(request, tag_slug):  # ф-я для отображения статей по определенному тегу
#     tag = get_object_or_404(TagPost, slug=tag_slug)  # берется запись из модели TagPost по slug
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")  # получить все публикованные
#     # статьи из posts + select_related
#
#     data = {  # передается в шаблон
#         'title': f"Тег: {tag.tag}",  # tag.tag, так как в class TagPost аргумент назван tag
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,  # выбранный пункт категории
#     }
#
#     return render(request, 'women/index.html', context=data)  # render + шаблон index + context
