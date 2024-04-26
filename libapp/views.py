from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
    Http404,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
)

from .models import Author, SeriesBook, Book
from .forms import AddAuthorForm, AddSeriesBookForm, AddBookForm


def main_page(request):
    return render(request, "libapp/main.html")


class CreateAuthor(LoginRequiredMixin, CreateView):
    form_class = AddAuthorForm
    template_name = "libapp/create.html"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_authors")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = {
            "authors": True,
            "author": False,
            "series_book": False,
            "book": False,
        }
        context["title"] = "Добавление автора"
        return context


class CreateSeriesBook(LoginRequiredMixin, CreateView):
    form_class = AddSeriesBookForm
    template_name = "libapp/create.html"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        author_id = self.kwargs.get("author_id")
        w.author = Author.objects.filter(pk=author_id).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "show_author", kwargs={"author_id": self.kwargs.get("author_id")}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = {
            "authors": False,
            "author": True,
            "series_book": False,
            "book": False,
        }
        author_id = self.kwargs.get("author_id")
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        context["author"] = author
        context["title"] = "Добавление серии"
        return context


class CreateBook(LoginRequiredMixin, CreateView):
    form_class = AddBookForm
    template_name = "libapp/create.html"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        series_book_id = self.kwargs.get("series_book_id")
        w.series = SeriesBook.objects.filter(pk=series_book_id).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "show_series_book",
            kwargs={
                "author_id": self.kwargs.get("author_id"),
                "series_book_id": self.kwargs.get("series_book_id"),
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = {
            "authors": False,
            "author": False,
            "series_book": True,
            "book": False,
        }
        author_id = self.kwargs.get("author_id")
        series_book_id = self.kwargs.get("series_book_id")
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
        context["author"] = author
        context["series_book"] = series_book
        context["title"] = "Добавление книги"
        return context


class ShowAuthors(LoginRequiredMixin, ListView):
    template_name = "libapp/show_authors.html"
    context_object_name = "authors"

    def get_queryset(self):
        return Author.undeleted.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторы'
        return context


class ShowAuthor(LoginRequiredMixin, ListView):
    template_name = "libapp/show_author.html"
    context_object_name = "series_book"

    def get_queryset(self):
        author = Author.undeleted.filter(pk=self.kwargs.get("author_id")).first()
        return SeriesBook.undeleted.filter(author=author).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_id = self.kwargs.get("author_id")
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        context["author"] = author
        context["delete"] = {
            "author": "author",
            "series_book": "series_book",
            "book": "book",
        }
        context['title'] = 'Автор'
        return context


class ShowSeriesBook(LoginRequiredMixin, ListView):
    template_name = "libapp/show_series_book.html"
    context_object_name = "books"

    def get_queryset(self):
        series = SeriesBook.undeleted.filter(
            pk=self.kwargs.get("series_book_id")
        ).first()
        return Book.undeleted.filter(series=series).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_id = self.kwargs.get("author_id")
        series_book_id = self.kwargs.get("series_book_id")
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
        context["author"] = author
        context["series_book"] = series_book
        context["delete"] = {
            "author": "author",
            "series_book": "series_book",
            "book": "book",
        }
        context['title'] = 'Серия'
        return context


class ShowBook(LoginRequiredMixin, DetailView):
    template_name = "libapp/show_book.html"
    pk_url_kwarg = "book_id"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_id = self.kwargs.get("author_id")
        series_book_id = self.kwargs.get("series_book_id")
        book_id = self.kwargs.get("book_id")
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
            raise Http404
        elif not Book.undeleted.filter(pk=book_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
        context["author"] = author
        context["series_book"] = series_book
        context["delete"] = {
            "author": "author",
            "series_book": "series_book",
            "book": "book",
        }
        context['title'] = 'Книга'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Book.undeleted, pk=self.kwargs.get(self.pk_url_kwarg))


class EditAuthorPage(LoginRequiredMixin, UpdateView):
    form_class = AddAuthorForm
    template_name = "libapp/create.html"
    pk_url_kwarg = "edit_id"

    def get_queryset(self):
        return Author.undeleted

    def get_success_url(self):
        return reverse(
            "show_author", kwargs={"author_id": self.kwargs.get("author_id")}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = {
            "authors": False,
            "author": True,
            "series_book": False,
            "book": False,
        }
        author_id = self.kwargs.get("author_id")
        edit = self.kwargs.get("edit")
        if not edit == "author" and not edit == "series_book" and not edit == "book":
            raise Http404
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        context["author"] = author
        context["title"] = "Редактирование автора"
        return context


class EditSeriesBookPage(LoginRequiredMixin, UpdateView):
    template_name = "libapp/create.html"
    pk_url_kwarg = "edit_id"

    def get_form_class(self):
        edit = self.kwargs.get("edit")
        if edit == "author":
            return AddAuthorForm
        elif edit == "series_book":
            return AddSeriesBookForm

    def get_queryset(self):
        edit = self.kwargs.get("edit")
        if edit == "author":
            return Author.undeleted
        elif edit == "series_book":
            return SeriesBook.undeleted

    def get_success_url(self):
        return reverse(
            "show_series_book",
            kwargs={
                "author_id": self.kwargs.get("author_id"),
                "series_book_id": self.kwargs.get("series_book_id"),
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = {
            "authors": False,
            "author": False,
            "series_book": True,
            "book": False,
        }
        author_id = self.kwargs.get("author_id")
        series_book_id = self.kwargs.get("series_book_id")
        edit = self.kwargs.get("edit")
        if not edit == "author" and not edit == "series_book" and not edit == "book":
            raise Http404
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
        context["author"] = author
        context["series_book"] = series_book
        context["title"] = "Редактирование серии"
        return context


class EditBookPage(LoginRequiredMixin, UpdateView):
    template_name = "libapp/create.html"
    pk_url_kwarg = "edit_id"

    def get_form_class(self):
        edit = self.kwargs.get("edit")
        if edit == "author":
            return AddAuthorForm
        elif edit == "series_book":
            return AddSeriesBookForm
        elif edit == "book":
            return AddBookForm

    def get_queryset(self):
        edit = self.kwargs.get("edit")
        if edit == "author":
            return Author.undeleted
        elif edit == "series_book":
            return SeriesBook.undeleted
        elif edit == "book":
            return Book.undeleted

    def get_success_url(self):
        return reverse(
            "show_book",
            kwargs={
                "author_id": self.kwargs.get("author_id"),
                "series_book_id": self.kwargs.get("series_book_id"),
                "book_id": self.kwargs.get("book_id"),
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = {
            "authors": False,
            "author": False,
            "series_book": False,
            "book": True,
        }
        author_id = self.kwargs.get("author_id")
        series_book_id = self.kwargs.get("series_book_id")
        book_id = self.kwargs.get("book_id")
        edit = self.kwargs.get("edit")
        if not edit == "author" and not edit == "series_book" and not edit == "book":
            raise Http404
        if not Author.undeleted.filter(pk=author_id).exists():
            raise Http404
        elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
            raise Http404
        elif not Book.undeleted.filter(pk=book_id).exists():
            raise Http404
        author = Author.undeleted.filter(pk=author_id).first()
        series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
        book = Book.undeleted.filter(pk=book_id).first()
        context["author"] = author
        context["series_book"] = series_book
        context["book"] = book
        context["title"] = "Редактирование книги"
        return context


@login_required
def delete_author_page(request, author_id, delete):
    if request.method == "POST":
        if request.POST.get("delete_button") == "delete":
            author = Author.undeleted.filter(pk=author_id).first()
            series_book = SeriesBook.undeleted.filter(author=author).all()
            for series in series_book:
                books = Book.undeleted.filter(series=series).all()
                for book in books:
                    book.is_deleted = True
                    book.save()
                series.is_deleted = True
                series.save()
            author.is_deleted = True
            author.save()
            url = reverse("show_authors")
            return redirect(url)
    if not delete == "author" and not delete == "series_book" and not delete == "book":
        raise Http404
    if not Author.undeleted.filter(pk=author_id).exists():
        raise Http404
    author = Author.undeleted.filter(pk=author_id).first()
    series_book = SeriesBook.undeleted.filter(author=author).all()
    title = "Удаление автора"
    return render(
        request,
        "libapp/delete_author.html",
        {"author": author, "series_book": series_book, "title": title},
    )


@login_required
def delete_series_book_page(request, author_id, series_book_id, delete):
    if request.method == "POST":
        if request.POST.get("delete_button") == "delete":
            if delete == "author":
                author = Author.undeleted.filter(pk=author_id).first()
                series_book = SeriesBook.undeleted.filter(author=author).all()
                for series in series_book:
                    books = Book.undeleted.filter(series=series).all()
                    for book in books:
                        book.is_deleted = True
                        book.save()
                    series.is_deleted = True
                    series.save()
                author.is_deleted = True
                author.save()
                url = reverse("show_authors")
                return redirect(url)
            elif delete == "series_book":
                series = SeriesBook.undeleted.filter(pk=series_book_id).first()
                books = Book.undeleted.filter(series=series).all()
                for book in books:
                    book.is_deleted = True
                    book.save()
                series.is_deleted = True
                series.save()
                url = reverse("show_author", args=(author_id,))
                return redirect(url)
    if not delete == "author" and not delete == "series_book" and not delete == "book":
        raise Http404
    if not Author.undeleted.filter(pk=author_id).exists():
        raise Http404
    elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
        raise Http404
    author = Author.undeleted.filter(pk=author_id).first()
    series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
    books = Book.undeleted.filter(series=series_book).all()
    if delete == 'author':
        title = "Удаление автора"
    else:
        title = "Удаление серии"
    return render(
        request,
        "libapp/delete_series_book.html",
        {
            "author": author,
            "series_book": series_book,
            "books": books,
            "delete": delete,
            "title": title,
        },
    )


@login_required
def delete_book_page(request, author_id, series_book_id, book_id, delete):
    if request.method == "POST":
        if request.POST.get("delete_button") == "delete":
            if delete == "author":
                author = Author.undeleted.filter(pk=author_id).first()
                series_book = SeriesBook.undeleted.filter(author=author).all()
                for series in series_book:
                    books = Book.undeleted.filter(series=series).all()
                    for book in books:
                        book.is_deleted = True
                        book.save()
                    series.is_deleted = True
                    series.save()
                author.is_deleted = True
                author.save()
                url = reverse("show_authors")
                return redirect(url)
            elif delete == "series_book":
                series = SeriesBook.undeleted.filter(pk=series_book_id).first()
                books = Book.undeleted.filter(series=series).all()
                for book in books:
                    book.is_deleted = True
                    book.save()
                series.is_deleted = True
                series.save()
                url = reverse("show_author", args=(author_id,))
                return redirect(url)
            elif delete == "book":
                book = Book.undeleted.filter(pk=book_id).first()
                book.is_deleted = True
                book.save()
                url = reverse(
                    "show_series_book",
                    args=(
                        author_id,
                        series_book_id,
                    ),
                )
                return redirect(url)
    if not delete == "author" and not delete == "series_book" and not delete == "book":
        raise Http404
    if not Author.undeleted.filter(pk=author_id).exists():
        raise Http404
    elif not SeriesBook.undeleted.filter(pk=series_book_id).exists():
        raise Http404
    elif not Book.undeleted.filter(pk=book_id).exists():
        raise Http404
    author = Author.undeleted.filter(pk=author_id).first()
    series_book = SeriesBook.undeleted.filter(pk=series_book_id).first()
    book = Book.undeleted.filter(pk=book_id).first()
    if delete == 'author':
        title = "Удаление автора"
    elif delete == 'series_book':
        title = "Удаление серии"
    else:
        title = "Удаление книги"
    return render(
        request,
        "libapp/delete_book.html",
        {
            "author": author,
            "series_book": series_book,
            "book": book,
            "delete": delete,
            "title": title
        },
    )
