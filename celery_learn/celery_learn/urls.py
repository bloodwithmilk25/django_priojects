"""celery_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.profile, name='profile')
Class-based views
    1. Add an import:  from other_app.views import profile
    2. Add a URL to urlpatterns:  path('', profile.as_view(), name='profile')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from publish.views import view_post, PostList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    re_path(r'^posts/(?P<slug>[a-zA-Z0-9\-]+)/$', view_post, name='view_post'),
    re_path(r'^$', PostList.as_view(), name='post_list')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
