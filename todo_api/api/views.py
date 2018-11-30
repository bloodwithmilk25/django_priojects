from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .models import Todo
from .serializers import TodosSerializer


class TodosListView(generics.ListAPIView):
    """
    GET todos/
    POST todos/
    """
    queryset = Todo.objects.all()
    serializer_class = TodosSerializer

    def post(self, request, *args, **kwargs):
        a_todo = Todo.objects.create(
            name=request.data["name"],
        )
        return Response(
            data=TodosSerializer(a_todo).data,
            status=status.HTTP_201_CREATED
        )


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET todos/:id/
    PUT todos/:id/
    DELETE todos/:id/
    """
    queryset = Todo.objects.all()
    serializer_class = TodosSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_todo = self.queryset.get(pk=kwargs["pk"])
            return Response(TodosSerializer(a_todo).data)
        except Todo.DoesNotExist:
            return Response(
                data={
                    "message": "Todo with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_todo = self.queryset.get(pk=kwargs["pk"])
            print('a_todo---------------', a_todo)
            print('a_todo---------------', request.data)  # {'completed': ['true']}
            serializer = TodosSerializer()
            updated_todo = serializer.update(a_todo, request.data)
            return Response(TodosSerializer(updated_todo).data)
        except Todo.DoesNotExist:
            return Response(
                data={
                    "message": "Todo with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_todo = self.queryset.get(pk=kwargs["pk"])
            a_todo.delete()
            return Response(data={"message": "Todo with id: {} was deleted".format(kwargs["pk"])},
                            status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response(
                data={
                    "message": "Todo with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )