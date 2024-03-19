from django import forms  # forms дает классы для формы
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women


@deconstructible  # (вариант валидатора 1 на уровне класса + декоратор) декоратор для создания валидатора
class RussianValidator:  # класс пользовательского валид-ра(удобен для частого общего использования) без базового класса
    AllOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "  # допустимые сим-ы
    code = 'russian'  # пользовательское название валидатора

    def __init__(self, message=None):  # инициализатор с одним параметром message=None
        self.message = message if message else "Должны присутствовать только русские символы, цифры, дефис, пробел."
        # атрибут с проверкой (Если передаем сообщение об ошибки - оно используется, если нет - выводится блок else)

    def __call__(self, value, *args, **kwargs):  # call вызывает проверку на корректность, если валидатор срабатывает
        if not (set(value) <= set(self.AllOWED_CHARS)):  # проверка на корректность вводимых символов из ALLOWED_CHARS
            raise ValidationError(self.message, code=self.code)  # исключение с сообщением об ошибке + передача code


"""" Формы связанные с моделями упрощают работу в целом, имеют встроенные методы из Джанго, более удобны. Пример ниже.
Это класс наследуемый от ModelForm, имеющий class Meta, свои валидаторы + form.save() """


class AddPostForm(forms.ModelForm):  # класс связан с моделью (служит для автоматизации полей формы)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    # Отображение поля в виде выпадающего списка
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем",
                                     label="Муж")  # empty_label - отображение надписи в пустом поле

    class Meta:  # вложенный класс Мета для привязки формы AddPostForm с моделью Women + имеет метод save()
        model = Women  # описывает связь формы с моделью Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband', 'tags']  # все поля берутся из
        # Women и указываются только те поля, которые есть в Women. Желательно прописывать конкретно отображаемые поля.
        widgets = {  # виджеты для поля заголовок и текст статьи
            'title': forms.TextInput(attrs={'class': 'form-input'}),  # поле, вид заполнения, стиль оформл-ия form-input
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),  # поле, вид заполнителя, 50 символов, 5 рядов
        }
        labels = {'slug': 'URL'}  # поле Slug отображается с названием URL

    def clean_title(self):  # Наш валидатор для проверки на корректность вводимых данных (не более 50 символов)
        title = self.cleaned_data['title']  # title получить из clean_data
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title

    # """ Вариант валидатора 2 на уровне метода - проще первого, подходит лучше для частной проверки"""
    # def clean_title(self):  # спец метод clean_имя поля для проверки (title в данном случае)
    #     title = self.cleaned_data['title']  # из словаря cleaned_data получаем значение по ключу title, далее проверка
    #     AllOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- "
    #
    #     if not (set(title) <= set(AllOWED_CHARS)):  # проверка на корректность вводимых символов из ALLOWED_CHARS
    #         raise ValidationError("Должны присутствовать только русские символы, цифры, дефис, пробел.")  # исключение


class UploadFileForm(forms.Form):  # класс не привязан к модели и формируется на базе Form(позволяет загружать файл)
    file = forms.ImageField(label='Файл')  # переменная file + тип поля(для img) + именная метка
