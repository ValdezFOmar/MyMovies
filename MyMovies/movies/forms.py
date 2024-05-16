from django import forms

from .models import MovieReview


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(dict(min=0, max=100)),
        }
