from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class UndeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class Author(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, default=None
    )
    name = models.CharField(max_length=100, blank=False)
    is_deleted = models.BooleanField(default=False)
    # series = models.ManyToManyField('SeriesBook', blank=True, null=True)

    objects = models.Manager()
    undeleted = UndeletedManager()
    deleted = DeletedManager()

    def get_absolute_url(self):
        return reverse("author", kwargs={"author_id": self.pk})


class SeriesBook(models.Model):
    class Status(models.IntegerChoices):
        UNCOMPLETE = 0, "Не завершено"
        COMPLETE = 1, "Завершено"

    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, default=None
    )
    name = models.CharField(max_length=255, blank=False)
    is_deleted = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(blank=True, default=0)
    is_completed = models.BooleanField(choices=Status.choices, blank=False)
    description = models.TextField(blank=True, null=True)
    # books = models.ManyToManyField('Book', null=True, blank=True)
    objects = models.Manager()
    undeleted = UndeletedManager()
    deleted = DeletedManager()

    def get_absolute_url(self):
        return reverse(
            "series_book", kwargs={"author_id": self.author.id, "series_id": self.pk}
        )


class Book(models.Model):
    class Status(models.IntegerChoices):
        UNCOMPLETE = 0, "Не завершено"
        COMPLETE = 1, "Завершено"

    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, default=None
    )
    name = models.CharField(max_length=255, blank=False)
    is_deleted = models.BooleanField(default=False)
    series = models.ForeignKey(SeriesBook, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(blank=True, default=0)
    is_completed = models.BooleanField(choices=Status.choices, blank=False)
    description = models.TextField(blank=True, null=True)
    # photo =

    objects = models.Manager()
    undeleted = UndeletedManager()
    deleted = DeletedManager()

    def get_absolute_url(self):
        return reverse(
            "book",
            kwargs={
                "author_id": self.series.author.id,
                "series_id": self.series.id,
                "book_id": self.pk,
            },
        )
