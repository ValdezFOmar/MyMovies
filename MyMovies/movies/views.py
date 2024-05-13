from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from movies.models import Movie

from .forms import NameForm


def index(request: HttpRequest):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, 'movies/index.html', context)


def login_user(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials, try again')
            return redirect('login-user')
    else:
        return render(request, 'movies/login.html')


def logout_user(request: HttpRequest):
    logout(request)
    messages.info(request, 'Logout successful')
    return redirect('index')


def movie_detail(request: HttpRequest, movie_id: int):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except ObjectDoesNotExist:
        raise Http404(f'Movie with id {movie_id} does not exists')
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
