from django import template  # импорт из Джанго модуль template
import women.views as views  # импорт из women.views с названием views
from women.models import Category, TagPost

register = template.Library()  # необходим для регистрации новых тегов


@register.inclusion_tag('women/list_categories.html')  # inclusion тэг формирует шаблон и возвр-т фрагмент HTML-страницы
def show_categories(cat_selected=0):  # ф-я возвращает обработанную HTML-страницу
    cats = Category.objects.all()  # вывод категорий и передача переменной cats
    return {'cats': cats, 'cat_selected': cat_selected}  # возвращает список cats_db по переменной cats
    # ф-я show_categories с аргументом cat_selected=0 дает выделение категории при наведении указателя


@register.inclusion_tag('women/list_tags.html')  # шаблонный тег для отображения тегов в левом сайдбаре
def show_all_tags():
    return {'tags': TagPost.objects.all()}  # возвращает все теги из модели TagPost

