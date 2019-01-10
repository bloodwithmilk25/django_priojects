from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .models import Cell
from .serializers import CellsSerializer


class CellsListView(generics.ListAPIView):
    """
    GET todos/
    """
    queryset = Cell.objects.all()
    serializer_class = CellsSerializer


class CellDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET todos/:id/
    PUT todos/:id/
    DELETE todos/:id/
    """
    queryset = Cell.objects.all()
    serializer_class = CellsSerializer

    def get(self, request, *args, **kwargs):
        try:
            cell = self.queryset.get(pk=kwargs["pk"])
            return Response(CellsSerializer(cell).data)
        except Cell.DoesNotExist:
            return Response(
                data={
                    "message": "Cell with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            cell = self.queryset.get(pk=kwargs["pk"])
            serializer = CellsSerializer()
            updated_todo = serializer.update(cell, request.data)
            return Response(CellsSerializer(updated_todo).data)
        except Cell.DoesNotExist:
            return Response(
                data={
                    "message": "Cell with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            cell = self.queryset.get(pk=kwargs["pk"])
            cell.delete()
            return Response(data={"message": "Cell with id: {} was deleted".format(kwargs["pk"])},
                            status=status.HTTP_204_NO_CONTENT)
        except Cell.DoesNotExist:
            return Response(
                data={
                    "message": "Cell with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )