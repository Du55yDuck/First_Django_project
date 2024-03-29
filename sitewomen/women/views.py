from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound  # импорт наших классов из django.http
from django.shortcuts import render, get_object_or_404  # импорт redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin

"""В классы добавлен DataMixin - благодаря наследованию передает стандартный функционал в классы, заметно уменьшает и 
убирает дублирование кода. Принято записывать первыми в списке наследования, так как они срабатывают первыми. Все
дополнительные классы принято содержать в директории приложения проекта в utils.py """


class WomenHome(DataMixin, ListView):  # класс типа ListView для отображения произвольных списков главной страницы.
    template_name = 'women/index.html'  # путь к шаблону, который используется
    context_object_name = 'posts'  # атрибут для использования списка статей из модели Women(posts в шаблоне index.html)
    title_page = 'Главная страница'  # title_page добавляется в словарь extra_context,кот-й формируется, благодаря Mixin
    cat_selected = 0  # Параметр выбора категории(маркер выделенной категории)

    def get_queryset(self):  # спец метод для отображения только опубликованных статей, если отображаются все статьи.
        return Women.published.all().select_related('cat')  # отображение всех опубликованных статей


def about(request):  # ф-я представления about(о сайте) + render ( 3 - аргумент в виде словаря в шаблоне about)
    contact_list = Women.published.all()  # Взять все опубликованные записи из модели Women
    paginator = Paginator(contact_list, 3)  # Класс Paginator, все опубл записи + кол-во элементов на странице

    page_number = request.GET.get('page')  # Через GET-запрос получить номер ('page') для отображения текущей страницы
    page_obj = paginator.get_page(page_number)  # получить текущую страницу по номеру (page_number)

    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})  # путь к шаблону + передача формы в шаблоны
    # about.html !(Джанго начинает поиск сверху)!


class ShowPost(DataMixin, DetailView):  # класс отображает выбранный пост + организация ссылки post_slug
    template_name = 'women/post.html'  # используемый шаблон
    slug_url_kwarg = 'post_slug'  # явно указана переменная, по которой вызывается статья(указать в urls.py - маршрутах)
    context_object_name = 'post'  # переменная из шаблона post.html

    def get_context_data(self, **kwargs):  # метод для вывода актуального заголовка в шапке выбранного поста
        context = super().get_context_data(**kwargs)  # вызов метода из базового класса
        return self.get_mixin_context(context, title=context['post'].title)  # Метод из Mixin с доп параметрами
        # Заголовок из словаря context по ключу context['post'].title с указанным ключом title.

    def get_object(self, queryset=None):  # отобразить статьи только из опубликованных записей, иначе исключение 404
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])  # Women.published - менеджер
    # записей(только публикованные), по slug-у через переменную slug_url_kwargs из ShowPost


class AddPage(DataMixin, CreateView):  # Class типа (CreateView) использует спец переменную
    # form в шаблоне addpage.html для взаимодействия. Иначе необходимо вносить изменения в шаблон.
    form_class = AddPostForm  # ссылка на сам класс AddPostForm(forms.py), а не на объект класса ()
    template_name = 'women/addpage.html'  # путь и имя используемого шаблона
    title_page = 'Добавление статьи'


class UpdatePage(DataMixin, UpdateView):  # Класс представления типа (UpdateView) для обновления статей
    model = Women  # связка с моделью Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']  # поля для обязательного заполнения
    template_name = 'women/addpage.html'  # путь к шаблону
    success_url = reverse_lazy('home')  # маршрут на главную страницу, после ввода данных в момент необходимости
    title_page = 'Редактирование статьи'


def contact(request):  # ф-я для контактов
    return HttpResponse("Обратная связь")


def login(request):  # ф-я для авторизации
    return HttpResponse("Авторизация")


class WomenCategory(DataMixin, ListView):  # Класс-аналог ф-и show_category (отображает список статей)
    template_name = 'women/index.html'  # шаблон для использования
    context_object_name = 'posts'  # использовать posts из шаблона index.html
    allow_empty = False  # атрибут действия при пустом списке(если указать не существующий slug - то вывод 404)

    def get_queryset(self):  # метод для отображения опубликованных статей
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # фильтр для отображения
    # статей по конкретному slug-у(kwargs передает переменную из urlpatterns[category/...] -> cat_slug)

    def get_context_data(self, **kwargs):  # метод для получения динамических данных (данные в момент запроса)
        context = super().get_context_data(**kwargs)  # вызов метода get_context_data из базового класса + параметры
        cat = context['posts'][0].cat  # posts передается из ListView(Для вывода категории по [0] индексу записи)
        return self.get_mixin_context(context,  # Вызов метода Mixin + получения нужных нам ключей
                                      title='Категория - ' + cat.name,  # строка в заголовке с названием
                                      cat_selected=cat.pk,  # Получение cat_selected (выбор категории по id)
                                      )


def page_not_found(request, exception):  # ф-я представления для несуществующих страниц(обязательный request + exc-n)
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')  # возврат экземпляра для вывода сообщения - аналог 404


class TagPostList(DataMixin, ListView):  # класс отображает статью по выбранному тегу
    template_name = 'women/index.html'  # путь к шаблону
    context_object_name = 'posts'  # использовать переменную posts из шаблона
    allow_empty = False  # 404 при не верном slug

    def get_context_data(self, *, object_list=None, **kwargs):  # метод для получения динамических данных
        context = super().get_context_data(**kwargs)  # вызов метода get_context_data из базового класса + параметры
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)  # метод из Mixin с нужными параметрами

    def get_queryset(self):  # выбор статей по указанным тегам
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
