from django.db import models
from django.conf import settings
from django.template.defaultfilters import default, slugify
from uuid import uuid4

User = settings.AUTH_USER_MODEL


class Picture(models.Model):
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pictures")
    photo = models.ImageField(upload_to ='files/', default="pic.jpg")
    like = models.ManyToManyField(User, related_name="user_like", through="Like")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"{self.user.email}."

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify('{}'.format(str(uuid4()).split('-')[4]))
        super(Picture, self).save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    picture_likes = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f"{self.user.email}."

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"{self.user.email}."
    
    def __str__(self):
         return f"{self.user.email}."


class FriendLists(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friend_lists")
    friends = models.ManyToManyRel(User, related_name="friend_lists")

    def __str__(self):
         return f"{self.user.email}."

