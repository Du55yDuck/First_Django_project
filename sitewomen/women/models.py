from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class PublishedManager(models.Manager):  # класс пользовательского менеджера для описания моделей
    def get_queryset(self):  # возвращает опубликованные посты(спец метод базового класса)
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)  # возвращает опубликованные статьи


class Women(models.Model):  # наш класс-модель с полями для таблицы
    class Status(models.IntegerChoices):  # класс для именовывания опубликованных/не опубликованных статей в виджете
        DRAFT = 0, 'Черновик'  # название-статус в виджете в виде кортежа с int
        PUBLISHED = 1, 'Опубликовано'  # - костыль в 20 строке - преобразует 1 и 0 в булевы значения

    title = models.CharField(max_length=255, verbose_name="Заголовок")  # Заголовок с максимальным кол-во символов
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug",  # связка с slug в urls
                            validators=[  # стандартные валидаторы для slug + сообщение
                                MinLengthValidator(5, message="Минимум 5 символов"),
                                MaxLengthValidator(100, message="Максимум 100 символов")])

    photo = models.ImageField(upload_to="photos/%y/%m/%d", default=None,  # поле для загрузки фото для постов +
                              blank=True, null=True, verbose_name="Фото")  # параметры загрузки(каталог, имя...)
    content = models.TextField(blank=True, verbose_name="Текст статьи")  # Поле для текста(статьи) с доступно пустым
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")  # авто заполнение времени
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")  # меняющееся при каждом изменении
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),  # Публикация +
                                       default=Status.DRAFT, verbose_name="Статус")  # костыль "опубликовано" в админке

    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    # вторичной модели(women) к первичной (category) через ForeignKey + 'Category'(т.к. задан раньше) +
    # on_delete=..PROTECT(запрет на удаление постов) + related_name с собственным названием для привязки к вторич модели
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Теги")  # many-to-many
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,  # вывести Null в поле, где были удалены данные
                                   null=True, blank=True, related_name='wuman', verbose_name="Муж")
    # Параметр husband для связи one-to-one модели Women со своими свойствами(пустые поля, значения null и т. д.) +
    # ко всем полям добавлен verbose_name для отображения в админ панели.
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,  # атрибут связывает конкретную статью с её
                               related_name='posts', null=True, default=None)  # Автором. Получение модели get_user_mo-l
    # Связь ForeignKey(многие к одному) + доп параметры персонального имени, обратного связывания.

    objects = models.Manager()  # пользовательский менеджер по умолчанию (работает, если published не активен)
    published = PublishedManager()  # пользовательский менеджер публикаций(да/нет)

    def __str__(self):  # ф-я возвращает главное поле при запросах
        return self.title

    class Meta:  # спец класс для сортировки полей модели Women с методом ordering и indexes + порядок сортировки
        verbose_name = "Известные женщины"  # заголовок для админки
        verbose_name_plural = "Известные женщины"  # заголовок во множественном числе (без -s)
        ordering = ['-time_create']  # порядок сортировки
        indexes = [  # список индексированных полей для ускорения сортировки
            models.Index(fields=['-time_create'])  # class Meta - для управления сортировкой на уровне класса
        ]

    def get_absolute_url(self):  # метод, формирующий url для каждой конкретной записи
        return reverse('post', kwargs={'post_slug': self.slug})  # ф-я reverse возвращает полноценный url адрес


class Category(models.Model):  # Модель Category в виде класса для связи many-to-one (нашей первичной модели category)
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")  # имя категории + индекс-е поле
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # поле для обращения по slug + index

    class Meta:  # мета класс для вывода класса Category в админ панель
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):  # метод вывода информации
        return self.name

    def get_absolute_url(self):  # метод для формирования URl адреса (см шаблон в list_categories.html)
        return reverse('category', kwargs={'cat_slug': self.slug})  # возвращает с помощью reverse маршрут по
# имени Category и выводить из таблицы по полю slug


class TagPost(models.Model):  # модель для тегов наследуем от класса Model
    tag = models.CharField(max_length=100, db_index=True)  # название тега(индексированное) + max длина 100 символов
    slug = models.SlugField(max_length=255, unique=True, db_index=True)  # поле для slug (уникален и индексирован)

    def __str__(self):  # метод для отображения названия тегов
        return self.tag

    def get_absolute_url(self):  # метод возвращает url для конкретного тега(также отвечает в админке-смотреть на сайте)
        return reverse('tag', kwargs={'tag_slug': self.slug})  # slug берется из бд и формируется маршрут


class Husband(models.Model):  # модель поля Husband с параметрами длины и типа водимых данных
    name = models.CharField(max_length=100)  # поля для Husband...
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):  # возвращает имя для наглядности
        return self.name


class UploadFiles(models.Model):  # класс для загрузки файлов с использованием модели
    file = models.FileField(upload_to='uploads_model')  # переменная с параметром(путь для загрузки файлов)


