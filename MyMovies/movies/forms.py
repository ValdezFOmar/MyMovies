from django import forms

from .models import MovieReview


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(dict(min=0, max=100)),
        }
