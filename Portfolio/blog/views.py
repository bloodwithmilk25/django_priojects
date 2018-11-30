from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog.models import Post
from blog.forms import CommentForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
# Create your views here.


class BlogPage(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'blog'
        return context

    def get_queryset(self):
        return Post.objects.filter(date__lte=timezone.now()).order_by(
                                                            '-date')


class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = 'blog'
        return context


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog/post_detail/{}'.format(post.pk))
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})


# Django REST framework

class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    class Meta:
        model = Post
        fields = ('name','text','date','url')

@api_view(['GET', 'POST', ])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'posts': reverse('blog:post-list', request=request),
    })

class PostList(generics.ListCreateAPIView):
    """
    API endpoint that represents a list of posts.
    """
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that represents a single post.
    """
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
