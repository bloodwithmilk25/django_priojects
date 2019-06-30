from rest_framework.viewsets import ModelViewSet
from .models import Movie, Director
from .serializers import MovieSerializer, DirectorSerializer, TagSerializer
from rest_framework_bulk import BulkModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
# Create your views here.

# chaining Q constraints
import operator
from functools import reduce
from django.db.models import Q

from .filters import MovieFilter


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    search_fields = 'title',
    filter_class = MovieFilter

    def get_serializer(self, *args, **kwargs):
        """Allowing for bulk create"""
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)

    @action(detail=True)
    def director(self, request, pk=None):
        movie = self.get_object()
        director = movie.director
        serializer = DirectorSerializer(instance=director)
        return Response(serializer.data)

    @action(detail=True)
    def tags(self, request, pk=None):
        movie = self.get_object()
        tags = movie.tags
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def carpenters(self, request):
        carpenters = self.queryset.filter(director__name="John Carpenter")
        serializer = MovieSerializer(carpenters, many=True)
        return Response(serializer.data)


class DirectorViewSet(BulkModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def filter_queryset(self, queryset):
        if self.request.method == 'DELETE':
            data = self.request.data
            if data:
                filter_params = [Q(**item) for item in data]
                queryset = queryset.filter(reduce(operator.or_, filter_params))
            return queryset

        return super().filter_queryset(queryset)

    def allow_bulk_destroy(self, qs, filtered):
        # custom logic here

        # default checks if the qs was filtered
        # qs comes from self.get_queryset()
        # filtered comes from self.filter_queryset(qs)
        return qs is not filtered
