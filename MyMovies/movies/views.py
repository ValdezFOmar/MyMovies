from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
)
from django.shortcuts import redirect, render
from django.utils import timezone
from movies.models import Movie, User

from .forms import MovieReviewForm

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Protocol, TypeAlias, TypeVar

    from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
    from django.db.models import QuerySet

    from .models import MovieReview

    T = TypeVar('T', covariant=True)

    ScoreWithHasReview: TypeAlias = tuple[list[float], list[bool]]
    RecommendationContext: TypeAlias = tuple[zip[tuple[Movie, float, bool]], bool]
    AnyUser: TypeAlias = AbstractBaseUser | AnonymousUser

    class IterLen(Protocol[T]):
        def __iter__(self) -> Iterator[T]: ...
        def __len__(self) -> int: ...


def calc_movie_score(reviews: IterLen[MovieReview]) -> float:
    length = len(reviews)
    if length == 0:
        return 0
    return sum(r.rating for r in reviews) / length


def get_user_recommendations(user: User) -> QuerySet[Movie]:
    reviewed_movies = Movie.objects.filter(moviereview__user_id=user)
    unreviewed_movies = Movie.objects.exclude(id__in=reviewed_movies)[:4]
    return unreviewed_movies


def score_with_has_review(movies: QuerySet[Movie]) -> ScoreWithHasReview:
    scores = []
    has_reviews = []
    for movie in movies:
        reviews = movie.moviereview_set.all()
        scores.append(calc_movie_score(reviews))
        has_reviews.append(bool(reviews))
    return scores, has_reviews


def recommendation_context(user: AnyUser) -> RecommendationContext:
    if not user.is_authenticated:
        return zip(), False
    assert isinstance(user, User)
    recommendations = get_user_recommendations(user)
    recomm_with_score = zip(recommendations, *score_with_has_review(recommendations))
    has_recommendations = bool(recommendations)
    return recomm_with_score, has_recommendations


def index(request: HttpRequest):
    movies = Movie.objects.order_by('-release_date')
    recommendations, has_recommendations = recommendation_context(request.user)

    context = {
        'movies': movies,
        'movies_with_score': zip(movies, *score_with_has_review(movies)),
        'recommendations': recommendations,
        'has_recommendations': has_recommendations,
    }
    return render(request, 'movies/index.html', context)


def user_page(request: HttpRequest, user_id: int) -> HttpResponse:
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        raise Http404(f'User with id {user_id} does not exists')
    reviews = user.moviereview_set.order_by('-date_time')

    recommendations, has_recommendations = recommendation_context(request.user)
    context = {
        'reviews': reviews,
        'page_user': user,
        'recommendations': recommendations,
        'has_recommendations': has_recommendations,
    }
    return render(request, 'movies/user_page.html', context)


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
    reviews = movie.moviereview_set.order_by('-date_time')
    score = calc_movie_score(reviews)
    recommendations, has_recommendations = recommendation_context(request.user)
    context = {
        'movie': movie,
        'reviews': reviews,
        'score': score,
        'recommendations': recommendations,
        'has_recommendations': has_recommendations,
    }
    return render(request, 'movies/movie_detail.html', context)


def review_form(request: HttpRequest, movie_id: int) -> HttpResponse:
    try:
        movie = Movie.objects.get(pk=movie_id)
    except ObjectDoesNotExist:
        raise Http404(f'Movie with id {movie_id} does not exists')
    return render(request, 'movies/review_form.html', {'movie': movie})


@login_required(login_url='user-login')
def submit_movie_review(request: HttpRequest, movie_id: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed('GET')

    form = MovieReviewForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest('Invalid/missing form values')

    try:
        movie = Movie.objects.get(pk=movie_id)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest(f'Movie with id {movie_id} does not exists')

    review = form.save(commit=False)
    review.date_time = timezone.now()
    review.user = request.user
    review.movie = movie
    review.save()

    reviews = movie.moviereview_set.order_by('-date_time')
    return render(request, 'movies/movie_reviews.html', {'reviews': reviews})
