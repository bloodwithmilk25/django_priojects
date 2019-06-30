from rest_framework.serializers import ModelSerializer
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    )
from .models import Movie, Director, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class DirectorSerializer(BulkSerializerMixin, ModelSerializer):
    class Meta:
        model = Director
        fields = "__all__"
        list_serializer_class = BulkListSerializer


class MovieSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = ('title', 'year', 'director', 'tags')
