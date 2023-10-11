from django.urls import path
from main.views import (show_main, add_book, show_xml, show_json, show_xml_by_id, show_json_by_id,
                         register, login_user, logout_user, add_book_amount, dec_book_amount,
                         remove_book, get_item_json, add_item_ajax, delete_item_ajax, add_book_amount_ajax,
                         dec_book_amount_ajax)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add_book', add_book, name='add_book'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_book_amount/<int:book_id>/', add_book_amount, name='add_book_amount'),
    path('dec_book_amount/<int:book_id>/', dec_book_amount, name='dec_book_amount'),
    path('remove_book/<int:book_id>/', remove_book, name='remove_book'),
    path('get-item/', get_item_json, name='get_item_json'),
    path('create-ajax/', add_item_ajax, name='add_item_ajax'),
    path('delete-ajax/<int:book_id>', delete_item_ajax, name='delete_item_ajax'),
    path('add-book-amount-ajax/<int:book_id>', add_book_amount_ajax, name='add_book_amount_ajax'),
    path('dec-book-amount-ajax/<int:book_id>', dec_book_amount_ajax, name='dec_book_amount_ajax'),
]