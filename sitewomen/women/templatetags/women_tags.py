from django import template  # импорт из Джанго модуль template
from django.db.models import Count

import women.views as views  # импорт из women.views с названием views
from women.models import Category, TagPost
from women.utils import menu

register = template.Library()  # необходим для регистрации новых тегов


@register.simple_tag  # Простой пользовательский тег для отображения меню в заголовке страниц.
def get_menu():  # Тег передает переменную menu в контекстный процессор.
    return menu


@register.inclusion_tag('women/list_categories.html')  # inclusion тэг формирует шаблон и возвр-т фрагмент HTML-страницы
def show_categories(cat_selected=0):  # ф-я возвращает обработанную HTML-страницу
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)  # вывод категорий, связанных с
    # определенными постами и передача переменной cats + отобрать total > 0
    return {'cats': cats, 'cat_selected': cat_selected}  # возвращает список cats_db по переменной cats
    # ф-я show_categories с аргументом cat_selected=0 дает выделение категории при наведении указателя


@register.inclusion_tag('women/list_tags.html')  # шаблонный тег для отображения тегов в левом сайдбаре
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}  # возвращает теги из модели
    # TagPost, которые связанны с определенными постами
