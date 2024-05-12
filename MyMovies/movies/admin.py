from django.contrib import admin
from movies.models import Movie, Genre, Job, Person, MovieCredit, MovieReview

admin.register(Movie)
admin.register(Genre)
admin.register(Job)
admin.register(Person)
admin.register(MovieCredit)
admin.register(MovieReview)
