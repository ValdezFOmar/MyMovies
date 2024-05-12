from django.contrib import admin
from movies.models import Genre, Job, Movie, MovieCredit, MovieReview, Person

admin.register(Movie)
admin.register(Genre)
admin.register(Job)
admin.register(Person)
admin.register(MovieCredit)
admin.register(MovieReview)
