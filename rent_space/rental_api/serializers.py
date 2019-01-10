from rest_framework import serializers
from .models import Cell


class CellsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ("row", "column", "taken", "occupied_by", "id")

    def update(self, instance, validated_data):
        instance.taken = validated_data.get("taken", instance.taken)
        instance.occupied_by = validated_data.get("occupied_by", instance.occupied_by)
        instance.save()
        return instance