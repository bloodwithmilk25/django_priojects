import django_filters

from .models import Movie, Director


class MovieFilter(django_filters.FilterSet):
    director = django_filters.CharFilter('director__name')

    class Meta:
        model = Movie
        fields = ('director', 'year')