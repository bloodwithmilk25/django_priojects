from django.urls import path, re_path
from .views import TodosListView, TodoDetailView

app_name = "api"

urlpatterns = [
    path('todos/', TodosListView.as_view(), name="todo_all"),
    re_path('todos/(?P<pk>\d+)/$', TodoDetailView.as_view(), name="todo_detail")
]