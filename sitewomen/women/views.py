from django.http import HttpResponse, HttpResponseNotFound, Http404  # импорт наших классов из django.http
from django.shortcuts import render, redirect, get_object_or_404  # импорт redirect

from .forms import AddPostForm
from .models import Women, Category, TagPost

# Наше представление в виде функции, формирующее внешний вид сайта

menu = [{'title': "О сайте", 'url_name': 'about'},  # список со словарей из названия пункта меню и названий маршрутов
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]


def index(request):  # request - ссылка на запрос HttpRequest
    posts = Women.published.all().select_related('cat')  # posts - реализация обращения к БД + filter для
    # published (все публикации) + оптимизация через select_related(жадная загрузка по внешнему ключу типа ForeignKey

    data = {  # словарь с данными из шаблона index.html работает с помощью render (для примера)
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,  # непосредственно читает данные из БД
        'cat_selected': 0,  # cat_selected из list_categories == 0, так как выделяются все рубрики для выделения
    }
    return render(request, 'women/index.html', context=data)  # аналог кода выше, но с render
    # (context=data - 3 аргумент с явным параметром) (нужно прописывать путь!)


def about(request):  # ф-я представления about(о сайте) + render ( 3 - аргумент в виде словаря в шаблоне about)
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})  # путь к шаблону
    # about.html !(Джанго начинает поиск сверху)!


def show_post(request, post_slug):  # ф-я для организации ссылки post_slug
    post = get_object_or_404(Women, slug=post_slug)  # выводит одну страницу по slug или 404 + импорт Women

    data = {  # передает заголовок статьи, меню, страницу
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'women/post.html', data)  # возвращает шаблон post.html и словарь data


def addpage(request):  # ф-я для добавления контента (возвращает шаблон addpage) + request.GET/POST - показывает инфо
    if request.method == 'POST':  # Проверка на POST запрос
        form = AddPostForm(request.POST)  # экземпляр класса нашей формы для отображения в шаблоне addpage.html + данные
        if form.is_valid():  # Если проверка на уровне сервера проходит с помощью метода is_valid
            # print(form.cleaned_data)  # выводит очищенные данные в консоль
            # try: сохранение данных в БД и вывод исключения в случае ошибки
            #     Women.objects.create(**form.cleaned_data) # Из модели Women.objects создать новый объект + распаковать
            #     return redirect('home')  # если статья добавлена успешно, то переход на главную страницу.
            # except: # словарь из clean_data(содержит набор всех необходимых полей)
            #      form.add_error(None, "Ошибка добавления поста") # вывод сообщения об ошибке
            form.save()  # метод аналог кода выше - сохраняет данные в ДБ women_women
            return redirect('home')  # перенаправление после записи на главную страницу
    else:
        form = AddPostForm()  # Иначе form с GET запросом возвращает form с пустыми полями(GET - уровень браузера)

    data = {  # вспомогательный словарь с данными
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form  # содержит либо form с данными(если POST-запрос), либо с пустыми полями(если GET-запрос)
    }
    return render(request, 'women/addpage.html', data)  # передача словаря


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


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404


def show_tag_postlist(request, tag_slug):  # ф-я для отображения статей по определенному тегу
    tag = get_object_or_404(TagPost, slug=tag_slug)  # берется запись из модели TagPost по slug
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")  # получить все публикованные
    # статьи из posts + select_related

    data = {  # передается в шаблон
        'title': f"Тег: {tag.tag}",  # tag.tag, так как в class TagPost аргумент назван tag
        'menu': menu,
        'posts': posts,
        'cat_selected': None,  # выбранный пункт категории
    }

    return render(request, 'women/index.html', context=data)  # render + шаблон index + context
