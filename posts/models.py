from django.db import models
from django.conf import settings


class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=3000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    # image = models.ImageField(upload_to='image', blank=True)
    category = models.CharField(max_length=20, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='image', blank=True)
    post = models.ForeignKey(
        Post,
        related_name='images',
        on_delete=models.CASCADE
    )


class Comment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.comment) > len_title:
            titlestring = self.comment[:len_title] + '...'
        else:
            titlestring = self.comment
        return titlestring
