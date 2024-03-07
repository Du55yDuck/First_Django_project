from django.contrib import admin
from .models import Women, Category


@admin.register(Women)  # декоратор register для регистрации админки + Women, наследуем от admin
class WomenAdmin(admin.ModelAdmin):  # класс для управления админ панелью со своими атрибутами
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat')  # поля для админ панели
    list_display_links = ('id', 'title')  # кликабельные поля(не может быть одновременно редактируемым и наоборот)
    ordering = ['-time_create', 'title',]  # сорт-ка только для админки по указан полям(2 поля, если 1 не соответствует)
    list_editable = ('is_published',)  # редактируемое поле Статус(is_published)
    list_per_page = 5  # пагинация списков на странице(мах кол-во полей на странице)


@admin.register(Category)
class WomenAdmin(admin.ModelAdmin):  # class Category для модели Категории в админ панели
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
