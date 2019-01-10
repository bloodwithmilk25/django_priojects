from django.urls import path, re_path
from .views import CellsListView, CellDetailView


app_name = 'api'

urlpatterns = [
    path('cells/', CellsListView.as_view(), name="cells"),
    re_path('cells/(?P<pk>\d+)/$', CellDetailView.as_view(), name="cell")
]