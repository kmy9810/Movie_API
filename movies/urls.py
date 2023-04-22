from django.urls import path
from .views import MovieList, MovieDetail, ReviewList

urlpatterns = [
    path('movies', MovieList.as_view()),
    path('movies/<int:pk>', MovieDetail.as_view()),
    path('movies/<int:pk>/reviews', ReviewList.as_view()),
]
