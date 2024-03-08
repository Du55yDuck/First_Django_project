from django.contrib import admin, messages
from .models import Women, Category


@admin.register(Women)  # декоратор register для регистрации админки + Women, наследуем от admin
class WomenAdmin(admin.ModelAdmin):  # класс для управления админ панелью со своими атрибутами
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')  # поля для админ панели
    list_display_links = ('title',)  # кликабельные поля(не может быть одновременно редактируемым и наоборот)
    ordering = ['-time_create', 'title',]  # сорт-ка только для админки по указан полям(2 поля, если 1 не соответствует)
    list_editable = ('is_published',)  # редактируемое поле Статус(is_published)
    list_per_page = 5  # пагинация списков на странице(мах кол-во полей на странице)
    actions = ['set_published', 'set_draft']  # спец атрибут для добавления нового действия

    @admin.display(description="Краткое описание", ordering='content')  # дек-ор меняет назв-е поля + сорт-ка по лексике
    def brief_info(self, women: Women):  # Метод создает новое пользовательское поле, women - объект модели Women
        return f"Описание {len(women.content)} символов."  # возвращает длину символов в статье

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
