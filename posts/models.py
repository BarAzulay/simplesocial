from __future__ import unicode_literals
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
import misaka

from groups.models import  Group
from django.contrib.auth import get_user_model
User = get_user_model()


from django.contrib.contenttypes.fields import GenericRelation

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


from django import template
register = template.Library()
from django.db.models.signals import pre_save
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify



class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)







class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts",null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    comment = GenericRelation(Comment)



    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.slug = slugify(self.message)
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

  #  def get_absolute_url(self):
   #     return reverse("posts:single", kwargs={"slug": self.slug})


    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    def get_posts_url(self):
        return reverse( "posts:single_2" , kwargs={"slug": self.group.slug})

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("message", "user")

    def get_like_url(self):
        return reverse("posts:like", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("posts:like-api-toggle", kwargs={"slug": self.slug})


