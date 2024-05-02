from django.contrib import admin

# Register your models here.

from .models import  Topic, Comment, User,Post,File

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(File)