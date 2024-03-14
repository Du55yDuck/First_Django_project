from django import forms  # forms дает классы для формы
from .models import Category, Husband


class AddPostForm(forms.Form):  # класс не связан с моделью для примера(служит для автоматизации полей формы)
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    # Атрибуты называются также как в модели для сохранения в БД в дальнейшем(связан с html-формой) + стиль 'form-input'
    slug = forms.SlugField(max_length=255, label="URL")  # label - меняет название поля
    content = forms.CharField(widget=forms.Textarea(attrs={'color': 50, 'rows': 5}), required=False, label="Контент")
    # widget для тонкой настройки отображения поля в html + Textarea(с заданными параметрами в отображаемых полях)
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")  # required=False - указывает на
    # необязательное заполнение поля + initial - авто галочка в поле при входе на страницу
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    # Отображение поля в виде выпадающего списка
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем",
                                     label="Муж")  # empty_label - отображение надписи в пустом поле
