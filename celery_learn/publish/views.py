from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post


def view_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Poll does not exist")

    post.view_count += 1
    post.save()

    return render(request, 'publish/post.html', context={'post': post})
