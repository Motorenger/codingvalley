import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from whatchlists.models import Movie


class Discussion(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=400)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="discussions")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="discussions", null=True, blank=True)

    class Meta:
        verbose_name = _("Discussion")
        verbose_name_plural = _("Discussions")

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    content = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content[:50]