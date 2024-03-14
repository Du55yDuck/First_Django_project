from django import forms  # forms дает классы для формы
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband


@deconstructible  # (варинат валидатора 1 на уровне класса + декоратор) декоратор для создания валидатора
class RussianValidator:  # класс пользовательского валид-ра(удобен для частого общего использования) без базового класса
    AllOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "  # допустимые сим-ы
    code = 'russian'  # пользовательское название валидатора

    def __init__(self, message=None):  # инициализатор с одним параметром message=None
        self.message = message if message else "Должны присутствовать только русские символы, цифры, дефис, пробел."
        # атрибут с проверкой (Если передаем сообщение об ошибки - оно используется, если нет - выводится блок else)

    def __call__(self, value, *args, **kwargs):  # метод call вызывает проверку на коррек-ть, если валидатор срабатывает
        if not (set(value) <= set(self.AllOWED_CHARS)):  # проверка на корректность вводимых символов из ALLOWED_CHARS
            raise ValidationError(self.message, code=self.code)  # исключение с сообщением об ошибке + передача code


class AddPostForm(forms.Form):  # класс не связан с моделью для примера(служит для автоматизации полей формы)
    title = forms.CharField(max_length=255, min_length=5,
                            label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form-input'}),  # меняет стиль вводимого текста
                            # validators=[RussianValidator()], - пользовательский валидатор(вариант 1)
                            error_messages={  # пользовательский валидатор сообщений об ошибках
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка хода нет',
                            })
    # Атрибуты называются также как в модели для сохранения в БД в дальнейшем(связан с html-формой) + стиль 'form-input'
    slug = forms.SlugField(max_length=255, label="URL",  # label - меняет название поля
                           validators=[  # стандартные валидаторы Джанго + пользовательские сообщения
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Максимум 100 символов"),
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'color': 50, 'rows': 5}), required=False, label="Контент")
    # widget для тонкой настройки отображения поля в html + Textarea(с заданными параметрами в отображаемых полях)
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")  # required=False - указывает на
    # необязательное заполнение поля + initial - авто галочка в поле при входе на страницу
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    # Отображение поля в виде выпадающего списка
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем",
                                     label="Муж")  # empty_label - отображение надписи в пустом поле

    """ Вариант валидатора 2 на уровне метода - проще первого, подходит лучше для частной проверки"""
    def clean_title(self):  # спец метод clean_имя поля для проверки (title в данном случае)
        title = self.cleaned_data['title']  # из словаря cleaned_data получаем значение по ключу title, далее проверка.
        AllOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "

        if not (set(title) <= set(AllOWED_CHARS)):  # проверка на корректность вводимых символов из ALLOWED_CHARS
            raise ValidationError("Должны присутствовать только русские символы, цифры, дефис, пробел.")  # исключение


