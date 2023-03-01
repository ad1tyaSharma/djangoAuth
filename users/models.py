from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Blogger(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.CharField(default='blogger',max_length=50)
    password = models.SlugField()
    profilePic = models.URLField(default='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png')
    # likes = ArrayField(models.ForeignKey(on_delete='cascade'), blank=True)
    def __str__(self):
        return self.name
