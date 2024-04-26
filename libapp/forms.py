from django import forms
from django.core.exceptions import ValidationError

from .models import Author, SeriesBook, Book


class AddAuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
        }
        labels = {"name": "Имя"}


class AddSeriesBookForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=0,
        max_value=10,
        label="Оценка",
        widget=forms.NumberInput(attrs={"class": "form-input"}),
    )

    class Meta:
        model = SeriesBook
        fields = ["name", "description", "rating", "is_completed"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input-area"}),
            # 'rating': forms.NumberInput(attrs={'class': 'form-input'}),
            "is_completed": forms.Select(attrs={"class": "form-input"}),
        }
        labels = {
            "name": "Название",
            "description": "Описание",
            # 'rating': 'Оценка',
            "is_completed": "Статус",
        }


class AddBookForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=0,
        max_value=10,
        label="Оценка",
        widget=forms.NumberInput(attrs={"class": "form-input"}),
    )

    class Meta:
        model = Book
        fields = ["name", "description", "rating", "is_completed"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input-area"}),
            # 'rating': forms.NumberInput(attrs={'class': 'form-input'}),
            "is_completed": forms.Select(attrs={"class": "form-input"}),
        }
        labels = {
            "name": "Название",
            "description": "Описание",
            # 'rating': 'Оценка',
            "is_completed": "Статус",
        }
