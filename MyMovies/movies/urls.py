from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie-detail'),
    path('get-name/', views.get_name, name='get-name'),
]
