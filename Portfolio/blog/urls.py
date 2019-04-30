from django.urls import re_path, include
from .views import BlogPage, PostDetailView, add_comment_to_post

app_name = 'blog'

urlpatterns = [
    re_path(r'^$', BlogPage.as_view(),name='bloghomepage'),
    re_path(r'(?P<pk>\d+)$', PostDetailView.as_view(), name='post_detail'),
    re_path(r'(?P<pk>\d+)/comment/$', add_comment_to_post, name='add_comment_to_post')
]