from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.TextField()
    creation_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
