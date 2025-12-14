# orm_model/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('author/create/', views.create_author, name='create_author'),
    path('book/create/', views.create_book, name='create_book'),
    path('author/<int:author_id>/', views.get_author, name='get_author'),
    path('book/<int:book_id>/', views.get_book, name='get_book'),
    path('author/update/<int:author_id>/', views.update_author, name='update_author'),
    path('book/update/<int:book_id>/', views.update_book, name='update_book'),
    path('author/delete/<int:author_id>/', views.delete_author, name='delete_author'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
