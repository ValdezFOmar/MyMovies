from django.http import HttpRequest
from django.shortcuts import render
from movies.models import Movie
from .forms import NameForm


def index(request: HttpRequest):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, 'movies/index.html', context)


def movie_detail(request: HttpRequest, movie_id: int):
    movie = Movie.objects.get(pk=movie_id)
    context = {'movie': movie}
    return render(request, 'movies/movie_detail.html', context)


def get_name(request: HttpRequest):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, 'movies/name-ok.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'movies/name.html', {'form': form})
