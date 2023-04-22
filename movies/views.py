from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import get_object_or_404
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination


class MoviePageNumberPagination(PageNumberPagination):
    page_size = 2


class MovieList(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePageNumberPagination


class MovieDetail(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewList(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        return Review.objects.filter(movie=movie)

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('pk'))
        serializer.save(movie=movie)
