from django.apps import AppConfig


class WomenConfig(AppConfig):
    verbose_name = "Женщины мира"  # заголовок в админке
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
