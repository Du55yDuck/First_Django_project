from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):  # класс для определения пользовательского фильтра
    title = 'Статус женщин'  # название фильтра
    parameter_name = 'status'  # переменная с названием status (в URL) содержит одно из значений метода lookups(mar/sin)

    def lookups(self, request, model_admin):  # метод возвращает список из возможных значений status(married/single)
        return [
            ('married', 'Замужем'),  # варианты возможных запросов
            ('single', 'Не замужем'),
        ]

    def queryset(self, request, queryset):  # метод для отбора найденных записей с условием замужем/не замужем
        if self.value() == 'married':  # если запрос == замужем
            return queryset.filter(husband__isnull=False)  # вернуть отфильтрованную коллекцию с husband != 0
        elif self.value() == 'single':  # если запрос == не замужем
            return queryset.filter(husband__isnull=True)  # вернуть кол-ю с условием husband == 0(Null)


@admin.register(Women)  # декоратор register для регистрации админки + Women, наследуем от admin
class WomenAdmin(admin.ModelAdmin):  # класс для управления админ панелью со своими атрибутами
    fields = ['title', 'slug', 'content', 'photo', 'post_photo', 'cat', 'husband', 'tags']  # Атриб для редактора статей
    # exclude = ['tags', 'is_published']  # атрибут для исключения указанных полей                      + указанные поля
    readonly_fields = ['post_photo']  # поля только для чтения + отображением мини-фото при добавлении
    prepopulated_fields = {"slug": ("title", )}  # атр-т для авто заполнения полей на основе других полей(slug по title)
    # filter_horizontal = ['tags'] настройка указанных полей в доп горизонтальном поле
    filter_vertical = ['tags']  # настройка указанных полей в доп вертикальном поле

    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')  # поля для админ панели
    list_display_links = ('title',)  # кликабельные поля(не может быть одновременно редактируемым и наоборот)
    ordering = ['-time_create', 'title',]  # сорт-ка только для админки по указан полям(2 поля, если 1 не соответствует)
    list_editable = ('is_published',)  # редактируемое поле Статус(is_published)
    list_per_page = 5  # пагинация списков на странице(мах кол-во полей на странице)

    actions = ['set_published', 'set_draft']  # спец атрибут для добавления нового действия
    search_fields = ['title__startswith', 'cat__name']  # атрибут - список нужных нам полей для поиска (заголовок +
    # lookup startswith(начало заголовка), категории + lookup name(название категории))
    list_filter = [MarriedFilter, 'cat__name', 'is_published']  # Поле для фильтра по указанным полям + ссылка на класс
    # MarriedFilter для подключения.
    save_on_top = True  # отображение панели сохранения наверху.

    @admin.display(description="Изображение:", ordering='content')  # дек-ор меняет назв-е поля +
    def post_photo(self, women: Women):
        if women.photo:  # Метод создает вычисляемое пользовательское поле, women - объект модели Women
            return mark_safe(f"<img src='{women.photo.url}' width=50>")  # mark_safe не экранирует HTML-теги, также
        return "Без фото"  # указать путь к мини-фото с шириной=50, либо выводит - Без фото.

    @admin.action(description="Опубликовать выбранные записи")  # декоратор меняющий название поля
    def set_published(self, request, queryset):  # метод для добавления действия в админ панель из выпадающего меню.
        count = queryset.update(is_published=Women.Status.PUBLISHED)  # request - объект запроса, queryset - набор
        # выбранных статей, update - обновляет статус опубликованных статей
        self.message_user(request, f"Изменено {count} записей")  # спец ф-я для вывода сообщения пользователю

    @admin.action(description="Снять с публикации выбранные записи")  # декоратор меняющий название поля
    def set_draft(self, request, queryset):  # метод для действия снятия с публикации в админ панель из выпадающего меню
        count = queryset.update(is_published=Women.Status.DRAFT)  # request - объект запроса, queryset - набор
        # выбранных статей, update - обновляет статус опубликованных статей, WARNING выводит спец символ в сообщении.
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(Category)
class WomenAdmin(admin.ModelAdmin):  # class Category для модели Категории в админ панели
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
