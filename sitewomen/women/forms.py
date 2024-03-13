from django import forms  # forms дает классы для формы
from .models import Category, Husband


class AddPostForm(forms.Form):  # класс не связан с моделью для примера(служит для автоматизации полей формы)
    title = forms.CharField(max_length=255)  # Атрибуты называются также для простоты как в модели(связан с html-формой)
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(), required=False)  # widget для тонкой настр-ки отобр-я поля в html
    is_published = forms.BooleanField(required=False)  # required=False - указывает на необязательное заполнение поля
    cat = forms.ModelChoiceField(queryset=Category.objects.all())  # Отображение поля в виде выпадающего списка
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False)
