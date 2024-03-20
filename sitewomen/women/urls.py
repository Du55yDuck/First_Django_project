from django.urls import path, register_converter  # импорт функций path, reg_converter из django.urls
from . import views  # импорт views из текущего модуля
from . import converters  # импорт из конверторов(наша папка с созданными конверторами)


register_converter(converters.FourDigitYearConverter, "year4")  # регистрация в Джанго нового конвертера с пом.
# специальной функции register_converter() c именем year4

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),  # http://127.0.0.1:8000 - маршр отвеч за гл стр + class WomenHome
    path('about/', views.about, name='about'),  # маршрут about(о сайте)
    path('addpage/', views.AddPage.as_view(), name='addpage'),  # маршр для поля с собств именем class AddPage + as_view
    path('contact/', views.contact, name='contact'),  # маршрут для поля с собственным именем contact
    path('login/', views.login, name='login'),  # маршрут для поля с собственным именем login
    path('post/<slug:post_slug>/', views.show_post, name='post'),  # маршрут для шаблона и ф-ии post(орг-я ссылки)+slug
    path('category/<slug:cat_slug>/', views.show_category, name='category'),  # маршрут с префиксом для category
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),  # маршрут tag/<slug..+ ф-я предст show_tag_pos..
]
