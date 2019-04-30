from django.views.generic import ListView, DetailView
from .models import Post
from .forms import CommentForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
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
