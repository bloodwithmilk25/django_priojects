from rest_framework import serializers
from .models import Todo


class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ("name", "completed", "created_date", 'id')

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)  # if there is no match
        #  in request for the 1st parameter, variable is set to the 2nd parameter
        instance.completed = validated_data.get("completed", instance.completed)
        if instance.completed is True or instance.completed is False:
            instance.save()
        else:
            instance.completed = instance.completed.title()
            instance.save()
        return instance