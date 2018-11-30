from django.urls import re_path, include
from blog.views import BlogPage,PostDetailView,add_comment_to_post,PostList,PostDetail,api_root
from rest_framework.urlpatterns import format_suffix_patterns
app_name = 'blog'

urlpatterns = [
    re_path(r'^$',BlogPage.as_view(),name='bloghomepage'),
    re_path(r'(?P<pk>\d+)$', PostDetailView.as_view(), name='post_detail'),
    re_path(r'(?P<pk>\d+)/comment/$', add_comment_to_post, name='add_comment_to_post'),
    # api related
    re_path(r'api/posts/(?P<pk>\d+)/$', PostDetail.as_view(), name='post-detail'),
    re_path(r'api/posts/$',PostList.as_view(), name='post-list'),
    re_path(r'api/',api_root, name='api_root'),
]


# api related
# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

# Default login/logout views
urlpatterns += [
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
