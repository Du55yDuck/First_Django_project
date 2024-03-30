menu = [{'title': "О сайте", 'url_name': 'about'},  # список из словарей - название пункта меню и название маршрута
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class DataMixin:  # Класс Миксин передает базовые данные в остальные дочерние классы
    paginate_by = 5  # управление пагинацией через атрибут paginate_by(кол-во элементов на странице)
    title_page = None  # Если не определен, то None
    cat_selected = None  # Если категория не выбрана (None)
    extra_context = {}  # Пустой словарь для наполнения из title_page из класса представления.

    def __init__(self):  # Инициализатор для наполнения словаря extra_context
        if self.title_page:  # Если title_page принимает значение не None, тогда в словарь extra_context через ключ
            self.extra_context['title'] = self.title_page  # ['title'] передаем значение title_page, далее в класс.

        if 'menu' not in self.extra_context:  # Если ключ 'меню' не в словаре, то присвоить его переменной menu
            self.extra_context['menu'] = menu

        if self.cat_selected is not None:  # Если категория не None(None = 0, а это False) Тогда сформировать ключ и
            self.extra_context['cat_selected'] = self.cat_selected  # присвоить переменной и далее в класс.

    def get_mixin_context(self, context, **kwargs):  # в метод передается dict для шаблона и некие параметры-(key:value)
        context['menu'] = menu  # расширение словаря стандартной инф-ей(меню, cat_selected + update)
        context['cat_selected'] = None
        context.update(kwargs)  # в словарь добавить содержимое kwargs
        return context  # вернуть обновленный словарь
