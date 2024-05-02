from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    qualification = models.CharField(max_length=200, null=True)
    avatar = models.ImageField(null=True, default="user.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
    

class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_IMAGE = 4
    FILE_TYPES = (
        (FILE_AUDIO, 'audio'),
        (FILE_VIDEO, 'video'),
        (FILE_PDF, 'pdf'),
        (FILE_IMAGE, 'image')
    )
    post = models.ForeignKey(Post, related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    file_type = models.PositiveSmallIntegerField(choices=FILE_TYPES)
    documents = models.ManyToManyField('self', related_name='files', symmetrical=False)
    file = models.FileField(upload_to='media/files/%Y/%m/%d/')
