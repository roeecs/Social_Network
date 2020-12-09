from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.TextField(blank=False)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likers')

    def __str__(self):
        return f'{self.writer.username} - {self.posted_at.strftime("%d/%m/%Y, %H:%M")}'

    @classmethod
    def add_post(cls, fields, writer):
        post = cls(content=fields['content'],
                   writer=writer)
        post.save()
        return post

    @classmethod
    def like(cls, fields, user):
        post = cls.objects.get(id=int(fields['post_id']))
        post.likes.add(user)
        post.save()
        return post

    @classmethod
    def unlike(cls, fields, user):
        post = cls.objects.get(id=int(fields['post_id']))
        post.likes.remove(user)
        post.save()
        return post

