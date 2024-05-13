from django.contrib import admin
from movies import models

admin.site.register(models.User)
admin.site.register(models.Movie)
admin.site.register(models.Genre)
admin.site.register(models.Job)
admin.site.register(models.Person)
admin.site.register(models.MovieCredit)
admin.site.register(models.MovieReview)
