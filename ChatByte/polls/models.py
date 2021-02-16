from django.db import models

class Posts(models.Model):
    id_str = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)

# Create your models here.


