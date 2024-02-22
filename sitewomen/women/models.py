from django.db import models


class Women(models.Model):  # наш класс-модель с полями для таблицы
    title = models.CharField(max_length=255)  # Заголовок с максимальным кол-во символов
    content = models.TextField(blank=True)  # Поле для текста(статьи) с доступно пустым
    time_create = models.DateTimeField(auto_now_add=True)  # Поле с авто заполнением времени в момент доб new записи
    time_update = models.DateTimeField(auto_now=True)  # Поле меняющееся при каждом изменении
    is_published = models.BooleanField(default=True)  # Поле публикации статьи(да/нет)

    def __str__(self):  # ф-я возвращает главное поле при запросах
        return self.title

    class Meta:  # спец класс для сортировки с методом ordering и indexes + порядок сортировки
        ordering = ['-time_create']  # порядок сортировки
        indexes = [  # список индексированных полей для ускорения сортировки
            models.Index(fields=['-time_create'])
        ]


