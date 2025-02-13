from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'







# apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'books'

    def ready(self):
        import books.signals
