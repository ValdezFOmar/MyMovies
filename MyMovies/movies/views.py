from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpRequest, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.utils import timezone
from movies.models import Movie

from .forms import MovieReviewForm


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
    form = MovieReviewForm()
    reviews = movie.moviereview_set.order_by('-date_time')
    context = {'movie': movie, 'review_form': form, 'reviews': reviews}
    return render(request, 'movies/movie_detail.html', context)


@login_required(login_url='user-login')
def submit_movie_review(request: HttpRequest, movie_id: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed('GET')

    form = MovieReviewForm(request.POST)

    if not form.is_valid():
        messages.error(request, 'Invalid/missing form values')
        return redirect('movie-detail', movie_id)

    try:
        movie = Movie.objects.get(pk=movie_id)
    except ObjectDoesNotExist:
        messages.error(request, f'Movie with id {movie_id} does not exists')
        return redirect('movie-detail', movie_id)

    review = form.save(commit=False)
    review.date_time = timezone.now()
    review.user = request.user
    review.movie = movie
    review.save()
    # TODO: Don't redirect, return HTML instead to be used with HTMX
    # This message (and the others) will need to be deleted then
    messages.success(request, f'Review for "{movie.title}" registered')
    return redirect('movie-detail', movie_id)
