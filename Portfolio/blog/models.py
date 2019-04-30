from django.db import models
from django.urls.base import reverse
from portf.models import Picture


class Post(models.Model):
    name = models.CharField(max_length=150)
    text = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Picture, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.post.pk})

    def __str__(self):
        return self.text
