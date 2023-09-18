from django.urls import path
from main.views import show_main, add_book

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add_book', add_book, name='add_book'),
]