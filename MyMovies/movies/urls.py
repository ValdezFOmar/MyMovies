from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie-detail'),
    path('movies/<int:movie_id>/review/submit', views.submit_movie_review, name='movie-review'),
    path('movies/<int:movie_id>/review/form', views.review_form, name='movie-review-form'),
    path('login-user/', views.login_user, name='login-user'),
    path('logout-user/', views.logout_user, name='logout-user'),
]
