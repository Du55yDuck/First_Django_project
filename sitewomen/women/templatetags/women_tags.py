from django import template  # импорт из Джанго модуль template
import women.views as views  # импорт из women.views с названием views


register = template.Library()  # необходим для регистрации новых тэгов


@register.simple_tag(name='getcats')  # декоратор register с использованием template. Library для создания simple_tag
def get_categories():  # ф-я-simple_tag возвращающая список категорий для наших постов
    return views.cats_db


@register.inclusion_tag('women/list_categories.html')  # inclusion тэг формирует шаблон и возвр-т фрагмент HTML-страницы
def show_categories(cat_selected=0):  # ф-я возвращает обработанную HTML-страницу
    cats = views.cats_db  # список cats_db будет возвращаться этим тэгом и передаваться по имени cats
    return {'cats': cats, 'cat_selected': cat_selected}  # возвращает список cats_db по переменной cats
    # ф-я show_categories с аргументом cat_selected=0 дает выделение категории при наведении указателя

