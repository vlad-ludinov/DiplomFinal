from django.urls import path
from . import views


urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("add_author/", views.CreateAuthor.as_view(), name="add_author"),
    path(
        "author/<int:author_id>/add_series_book/",
        views.CreateSeriesBook.as_view(),
        name="add_series_book",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/add_book/",
        views.CreateBook.as_view(),
        name="add_book",
    ),
    path("authors/", views.ShowAuthors.as_view(), name="show_authors"),
    path(
        "author/<int:author_id>/series_book/",
        views.ShowAuthor.as_view(),
        name="show_author",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/books",
        views.ShowSeriesBook.as_view(),
        name="show_series_book",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/book/<int:book_id>/",
        views.ShowBook.as_view(),
        name="show_book",
    ),
    path(
        "author/<int:author_id>/edit/<str:edit>/<int:edit_id>/",
        views.EditAuthorPage.as_view(),
        name="edit_author_page",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/edit/<str:edit>/<int:edit_id>/",
        views.EditSeriesBookPage.as_view(),
        name="edit_series_book_page",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/book/<int:book_id>/edit/<str:edit>/<int:edit_id>/",
        views.EditBookPage.as_view(),
        name="edit_book_page",
    ),
    path(
        "author/<int:author_id>/delete/<str:delete>/",
        views.delete_author_page,
        name="delete_author_page",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/delete/<str:delete>/",
        views.delete_series_book_page,
        name="delete_series_book_page",
    ),
    path(
        "author/<int:author_id>/series_book/<int:series_book_id>/book/<int:book_id>/delete/<str:delete>/",
        views.delete_book_page,
        name="delete_book_page",
    ),
]
