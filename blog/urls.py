from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("manage/", views.manage_blog, name="manage_blog"),
    path("add-article-page/", views.add_article_page, name="add_article_page"),
    path("add-article/", views.add_article, name="add_article"),
    path("delete-article/<int:id>/", views.delete_article, name="delete_article"),
    path("books/delete/<int:book_id>/", views.delete_book, name="delete_book"),
    path("article/<int:id>/", views.article_detail, name="article_detail"),

]

