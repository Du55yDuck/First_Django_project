from django.urls import path, register_converter  # импорт функций path, reg_converter из django.urls
from . import views  # импорт views из текущего модуля
from . import converters  # импорт из конверторов(наша папка с созданными конверторами)


register_converter(converters.FourDigitYearConverter, "year4")  # регистрация в Джанго нового конвертера с пом.
# специальной функции register_converter() c именем year4

urlpatterns = [
    path('', views.index),  # http://127.0.0.1:8000 - маршрут отвечает за главную страницу
    path('cats/<int:cat_id>/', views.categories),  # http://127.0.0.1:8000/cats/2/ - маршрут за страницу cats +
    # конвертер int с добавлением целого числа в конец адреса
    path('cats/<slug:cat_slug>/', views.categories_by_slug),  # конвертер для смешанных значений(числовые + строчные) ->
    #  !отрабатывает в порядке записи сверху-вниз(сперва cat_id, далее slug) по Джанго!(slug - более общий конвертер)
    path("archive/<year4:year>/", views.archive),  # маршрут и конвертер archive/year4 - принимающий 4 цифры как дату
]