from django.contrib import admin

from .models import Picture, Like, Comment

admin.site.register(Picture)
admin.site.register(Like)
admin.site.register(Comment)
