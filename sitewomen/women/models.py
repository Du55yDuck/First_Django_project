from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):  # класс пользовательского менеджера для описания моделей
    def get_queryset(self):  # возвращает опубликованные посты(спец метод базового класса)
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)  # возвращает опубликованные статьи


class Women(models.Model):  # наш класс-модель с полями для таблицы
    class Status(models.IntegerChoices):  # класс для именовывания опубликованных/не опубликованных статей в виджете
        DRAFT = 0, 'Черновик'  # название-статус в виджете в виде кортежа с int
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)  # Заголовок с максимальным кол-во символов
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # поле для связки с slug в urls
    content = models.TextField(blank=True)  # Поле для текста(статьи) с доступно пустым
    time_create = models.DateTimeField(auto_now_add=True)  # Поле с авто заполнением времени в момент доб new записи
    time_update = models.DateTimeField(auto_now=True)  # Поле меняющееся при каждом изменении
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)  # Поле публикации + choices
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts')  # параметр для связки
    # вторичной модели(women) к первичной (category) через ForeignKey + 'Category'(т.к. задан раньше) +
    # on_delete=..PROTECT(запрет на удаление постов) + related_name с собственным названием для привязки к вторич модели

    objects = models.Manager()  # пользовательский менеджер по умолчанию (работает, если published не активен)
    published = PublishedManager()  # пользовательский менеджер публикаций(да/нет)

    def __str__(self):  # ф-я возвращает главное поле при запросах
        return self.title

    class Meta:  # спец класс для сортировки с методом ordering и indexes + порядок сортировки
        ordering = ['-time_create']  # порядок сортировки
        indexes = [  # список индексированных полей для ускорения сортировки
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):  # метод, формирующий url для каждой конкретной записи
        return reverse('post', kwargs={'post_slug': self.slug})  # ф-я reverse возвращает полноценный url адрес


class Category(models.Model):  # Модель Category в виде класса для связи many-to-one (нашей первичной модели category)
    name = models.CharField(max_length=100, db_index=True)  # имя категории + индексированное поле
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # поле для обращения по slug + index

    def __str__(self):  # метод вывода информации
        return self.name

    def get_absolute_url(self):  # метод для формирования URl адреса (см шаблон в list_categories.html)
        return reverse('category', kwargs={'cat_slug': self.slug})  # возвращает с помощью reverse маршрут по
# имени Category и выводить из таблицы по полю slug

