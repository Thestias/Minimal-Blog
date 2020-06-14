from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class BlogPost(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    text_mark = models.TextField()
    created_time = models.CharField(max_length=200)

    def get_timestamp(self):
        ''' Used to add a timestamp when creating a blog'''

        now = datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M")

        return dt_string

    def __str__(self):
        return self.title
