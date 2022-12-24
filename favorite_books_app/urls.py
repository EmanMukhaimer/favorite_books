from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books', views.display_books),
    path('user_page', views.display_user_page),
    path('register', views.register),
    path('login', views.login),
    path('add_book', views.add_book),
    path('delete_book/<int:number>', views.delete_book, name="delete_book"),
    path('books/<int:number>', views.view_book, name="books"),
    path('update_book/<int:number>', views.update_book, name="update_book"),
    path('add_fav/<int:book_id>/<int:user_id>', views.add_fav, name='add_fav'),
    path('remove_fav/<int:book_id>/<int:user_id>', views.remove_fav, name='remove_fav'),
    path('logout', views.logout),
]