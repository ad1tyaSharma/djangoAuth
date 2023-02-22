from django.db import models
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.CharField(default='blogger',max_length=50)
    password = models.SlugField()
    profilePic = models.URLField(default='https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_1280.png')
