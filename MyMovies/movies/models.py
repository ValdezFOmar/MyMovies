from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    id: int
    moviereview_set: models.Manager[MovieReview]  # Only for type hinting

    def __str__(self) -> str:
        return f'ID<{self.id}> {self.username}'


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    moviereview_set: models.Manager[MovieReview]  # Only for type hinting

    title = models.CharField(max_length=200)
    overview = models.TextField()
    release_date = models.DateTimeField()
    running_time = models.IntegerField()
    budget = models.IntegerField(blank=True)
    tmdb_id = models.IntegerField(blank=True, unique=True)
    revenue = models.IntegerField(blank=True)
    poster_path = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Person, through='MovieCredit')

    def __str__(self) -> str:
        return self.title


class MovieCredit(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)


class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    review = models.TextField(blank=True)
    date_time = models.DateTimeField(blank=True)  # Auto generated
